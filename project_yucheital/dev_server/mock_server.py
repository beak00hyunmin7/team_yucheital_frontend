"""유체이탈 프론트엔드 테스트용 가짜(mock) AI 서버.

진짜 AI 모델 서버(team_yucheital_ai_model / terrainFlowSim/webapp)와 **같은 주소·같은 응답 형식**으로
대답하지만, U-Net 대신 간단한 규칙(낮은 곳에 물이 고인다)으로 그럴듯한 그림을 만든다.
torch · 체크포인트 · MySQL 없이 화면 기능 전체(샘플, 예측, 결과, 로그인, 기록)를 확인하는 용도.

필요한 것: Python 3.10+, Pillow, numpy  (pip install pillow numpy)

실행:
    python mock_server.py                 # http://127.0.0.1:8000 , 로그인 없이 예측 가능
    python mock_server.py --require-login  # 진짜 서버에서 DB 가 켜진 상황처럼 로그인 필수
    python mock_server.py --port 8100 --no-browser
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import secrets
import sys
import threading
import time
import uuid
import webbrowser
from email.parser import BytesParser
from datetime import datetime, timezone
from email.policy import default as email_policy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FRONTEND_DIR = HERE.parent / "yuche_frontend"
SAMPLES_DIR = HERE.parents[1] / "data" / "contours"      # sejong_yucheital_project/data/contours
TEST_INPUT_DIR = HERE / "test_inputs"

RAIN_RANGE = [20.0, 80.0]
TIME_RANGE = [0.0, 120.0]
DEFAULT_TIME_S = 18.0
DEFAULT_DX_M = 10.4166667
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
CHECKPOINT = "mock_best.pt (테스트 서버)"

USERS: dict[str, str] = {}      # email -> sha256(password)
TOKENS: dict[str, str] = {}     # token -> email
HISTORY: dict[str, list[dict]] = {}   # email -> 기록 (최신순). 서버를 끄면 사라짐
HISTORY_MAX = 50
LOCK = threading.Lock()
REQUIRE_LOGIN = False

# --------------------------------------------------------------------------- #
# 색상표: matplotlib 'terrain' 과 'Blues' 를 대략 흉내 (진짜 서버의 그림과 비슷하게 보이도록)
# --------------------------------------------------------------------------- #
_TERRAIN_STOPS = [(0.00, (51, 51, 153)), (0.15, (0, 153, 255)), (0.25, (0, 204, 102)),
                  (0.50, (255, 255, 153)), (0.75, (128, 92, 84)), (1.00, (255, 255, 255))]
_BLUES_STOPS = [(0.0, (247, 251, 255)), (0.35, (158, 202, 225)), (0.7, (49, 130, 189)), (1.0, (8, 48, 107))]


def _lut(stops, n=256) -> np.ndarray:
    xs = np.linspace(0, 1, n)
    px = [s[0] for s in stops]
    return np.stack([np.interp(xs, px, [s[1][c] for s in stops]) for c in range(3)], axis=1)


TERRAIN_LUT = _lut(_TERRAIN_STOPS)
try:
    FONT = ImageFont.truetype("malgun.ttf", 16)       # Windows 맑은 고딕 (한글)
except OSError:
    FONT = ImageFont.load_default()
BLUES_LUT = _lut(_BLUES_STOPS)


def colorize(values01: np.ndarray, lut: np.ndarray) -> Image.Image:
    idx = np.clip((values01 * (len(lut) - 1)).round().astype(int), 0, len(lut) - 1)
    return Image.fromarray(lut[idx].astype(np.uint8), "RGB")


def elevation_from_contour_image(img: Image.Image) -> np.ndarray:
    """채색 등고선 그림의 색을 terrain 색상표에서 가장 가까운 값으로 바꿔 대략적인 고도(0~1)를 얻는다."""
    small = np.asarray(img.convert("RGB").resize((128, 128)), dtype=np.float32)
    flat = small.reshape(-1, 1, 3)
    lut = TERRAIN_LUT[::4].reshape(1, -1, 3)            # 64단계면 충분
    nearest = np.argmin(((flat - lut) ** 2).sum(axis=2), axis=1)
    return (nearest / 63.0).reshape(128, 128)


def render_contour(terrain: np.ndarray) -> Image.Image:
    """고도 격자 -> 학습 데이터와 비슷한 '채색 20단계 + 검은 등고선' 그림 (256×256)."""
    t = terrain.astype(np.float32)
    t = (t - t.min()) / (np.ptp(t) or 1.0)
    t = np.asarray(Image.fromarray(t, "F").resize((256, 256), Image.BILINEAR))
    levels = np.floor(np.clip(t, 0, 0.999) * 20) / 20
    img = colorize(levels, TERRAIN_LUT)
    edges = np.asarray(Image.fromarray((levels * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)) > 0
    arr = np.asarray(img).copy()
    arr[edges] = (arr[edges] * 0.25).astype(np.uint8)
    return Image.fromarray(arr).transpose(Image.FLIP_TOP_BOTTOM)   # 진짜 서버처럼 Y축 위쪽


def fake_depth(elev: np.ndarray, rain_mm: float, time_s: float) -> np.ndarray:
    """낮을수록, 비가 많을수록, 시간이 짧을수록(물이 빠지기 전) 깊게. 0~1."""
    low = (1.0 - elev) ** 3
    rain_f = (rain_mm - RAIN_RANGE[0]) / (RAIN_RANGE[1] - RAIN_RANGE[0]) * 0.7 + 0.3
    time_f = np.exp(-max(time_s - 18.0, 0.0) / 90.0) * (0.6 + 0.4 * min(time_s, 18.0) / 18.0)
    d = Image.fromarray((np.clip(low, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
    d = np.asarray(d, dtype=np.float32) / 255.0
    return d * rain_f * time_f * 1.4   # 0~1 을 넘을 수 있음 (그림 그릴 때만 자른다)


def load_terrain(raw: bytes, filename: str) -> tuple[np.ndarray, dict]:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    meta: dict = {"source_format": ext}
    if ext == "npy":
        arr = np.load(io.BytesIO(raw), allow_pickle=False)
    elif ext in {"csv", "txt", "dat", "asc", "grd"}:
        lines = raw.decode("utf-8", errors="replace").splitlines()
        header = {}
        while lines and lines[0].split() and lines[0].split()[0].replace("_", "").isalpha():
            k, *v = lines.pop(0).split()
            header[k.lower()] = v[0] if v else ""
        if "cellsize" in header:
            meta["cellsize_m"] = float(header["cellsize"])
        sep = "," if "," in (lines[0] if lines else "") else None
        arr = np.array([[float(x) for x in (ln.split(sep))] for ln in lines if ln.strip()])
    elif ext in {"png", "jpg", "jpeg", "tif", "tiff"}:
        arr = np.asarray(Image.open(io.BytesIO(raw)).convert("L"), dtype=np.float64)
    else:
        raise ValueError(f"지원하지 않는 형식입니다: .{ext}")
    if arr.ndim != 2 or min(arr.shape) < 8:
        raise ValueError(f"2차원 고도 격자가 아닙니다 (shape={arr.shape})")
    meta["shape"] = list(arr.shape)
    return arr.astype(np.float64), meta


def b64png(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def predict(mode: str, raw: bytes, filename: str, rain_mm: float, time_s: float, dx: float) -> dict:
    meta: dict = {"mode": mode, "filename": filename}
    terrain = None
    if mode == "image":
        contour = Image.open(io.BytesIO(raw)).convert("RGB").resize((256, 256))
        meta["source_format"] = "contour_image"
        elev = elevation_from_contour_image(contour)
    else:
        terrain, tmeta = load_terrain(raw, filename)
        meta.update(tmeta)
        meta["dx_m"] = float(tmeta.get("cellsize_m") or dx)
        contour = render_contour(terrain)
        elev = np.flipud(np.asarray(Image.fromarray(((terrain - terrain.min()) / (np.ptp(terrain) or 1) * 255)
                                                    .astype(np.uint8)).resize((128, 128)), dtype=np.float32) / 255)

    rain_used = float(np.clip(rain_mm, *RAIN_RANGE))
    time_used = float(np.clip(time_s, *TIME_RANGE))
    meta.update({"rain_conditioned": True, "rain_mm": rain_used, "time_conditioned": True, "time_s": time_used})

    raw_depth = fake_depth(elev, rain_used, time_used)
    depth = np.clip(raw_depth, 0, 1)
    pred = colorize(depth, BLUES_LUT).resize((256, 256), Image.BILINEAR)
    alpha = Image.fromarray((np.clip(depth * 1.6, 0, 0.85) * 255).astype(np.uint8)).resize((256, 256), Image.BILINEAR)
    overlay = contour.copy()
    overlay.paste(pred, (0, 0), alpha)

    result = {
        "contour_png_base64": b64png(contour),
        "prediction_png_base64": b64png(pred),
        "overlay_png_base64": b64png(overlay),
        "analysis_png_base64": None,
        "drain_candidate": None,
        "checkpoint": CHECKPOINT,
        "meta": meta,
        "notes": [
            "⚠ 테스트용 가짜 서버의 결과입니다. 실제 U-Net 예측이 아니라 '낮은 곳에 물이 고인다'는 규칙으로 만든 그림이에요.",
            "예측 배수맵은 색이 진한(파란) 곳일수록 지표 유출수가 모이는 침수·배수 취약 지점입니다.",
        ],
    }

    if mode == "terrain":
        h, w = terrain.shape
        d_full = np.flipud(np.asarray(Image.fromarray(raw_depth.astype(np.float32), "F").resize((w, h), Image.BILINEAR)))
        r, c = np.unravel_index(int(np.argmax(d_full)), d_full.shape)
        analysis = overlay.copy().resize((512, 512))
        draw = ImageDraw.Draw(analysis)
        px, py = (c + 0.5) / w * 512, (1 - (r + 0.5) / h) * 512
        draw.ellipse([px - 12, py - 12, px + 12, py + 12], outline=(229, 72, 77), width=4)
        draw.rectangle([0, 0, 512, 30], fill=(255, 255, 255))
        draw.text((10, 6), f"배수구 후보 ({c}, {r}) · 강우 {rain_used:.0f}mm · 경과 {time_used:.0f}초 · 테스트 서버",
                  fill=(20, 20, 20), font=FONT)
        result["analysis_png_base64"] = b64png(analysis)
        result["drain_candidate"] = {
            "pixel": {"x": int(c), "y": int(r)},
            "normalized": {"x": round(c / max(w - 1, 1), 4), "y": round(r / max(h - 1, 1), 4)},
            # 화면 그림 위 위치 (왼쪽 위 = 0, 0). 그림은 terrain 배열과 상하가 반대라서 y 를 뒤집는다
            "image": {"x": round(c / max(w - 1, 1), 4), "y": round(1 - r / max(h - 1, 1), 4)},
        }
    else:
        h, w = raw_depth.shape
        r, c = np.unravel_index(int(np.argmax(raw_depth)), raw_depth.shape)
        pos = {"x": round(c / max(w - 1, 1), 4), "y": round(r / max(h - 1, 1), 4)}
        result["drain_candidate"] = {"pixel": {"x": int(c), "y": int(r)}, "normalized": pos, "image": pos}
    return result


def make_test_inputs() -> None:
    """'등고선 데이터' 모드 시험용 고도 격자 파일을 만든다 (없을 때만)."""
    TEST_INPUT_DIR.mkdir(exist_ok=True)
    npy = TEST_INPUT_DIR / "test_terrain_96x96.npy"
    asc = TEST_INPUT_DIR / "test_terrain_96x96.asc"
    if npy.exists() and asc.exists():
        return
    y, x = np.mgrid[0:96, 0:96] / 95.0
    z = (60 * np.exp(-((x - 0.3) ** 2 + (y - 0.7) ** 2) / 0.05)      # 언덕
         + 35 * np.exp(-((x - 0.75) ** 2 + (y - 0.35) ** 2) / 0.08)  # 작은 언덕
         - 20 * np.exp(-((x - 0.6) ** 2 + (y - 0.8) ** 2) / 0.02)    # 웅덩이
         + 15 * x + 10)
    np.save(npy, z)
    with open(asc, "w", encoding="ascii") as f:
        f.write(f"ncols 96\nnrows 96\nxllcorner 0\nyllcorner 0\ncellsize {DEFAULT_DX_M}\nNODATA_value -9999\n")
        for row in z:
            f.write(" ".join(f"{v:.3f}" for v in row) + "\n")


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    server_version = "YucheMock/1.0"

    def log_message(self, fmt, *args):
        sys.stdout.write(f"  {self.command:6} {self.path.split('?')[0]:28} {args[1] if len(args) > 1 else ''}\n")

    # ---- 공통 응답 ----
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, detail):
        self._json({"detail": detail}, status)

    def _file(self, path: Path, ctype: str):
        data = path.read_bytes()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _user(self) -> str | None:
        auth = self.headers.get("Authorization", "")
        return TOKENS.get(auth[7:]) if auth.startswith("Bearer ") else None

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    # ---- 분석 기록 (진짜 서버 history.py 와 같은 주소·형식, 저장만 메모리에) ----
    def _history_user(self) -> str | None:
        user = self._user()
        if not user:
            self._error(401, "로그인이 필요합니다.")
        return user

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_PATCH(self):
        path = urlparse(self.path).path
        if not path.startswith("/api/history/"):
            return self._error(404, "없는 주소입니다.")
        user = self._history_user()
        if not user:
            return
        record_id = path.rsplit("/", 1)[-1]
        name = (self._read_json().get("name") or "").strip() or None
        with LOCK:
            for rec in HISTORY.get(user, []):
                if rec["id"] == record_id:
                    rec["name"] = name
                    return self._json(rec)
        self._error(404, "기록을 찾을 수 없습니다.")

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path != "/api/history" and not path.startswith("/api/history/"):
            return self._error(404, "없는 주소입니다.")
        user = self._history_user()
        if not user:
            return
        with LOCK:
            records = HISTORY.get(user, [])
            if path == "/api/history":
                HISTORY[user] = []
                return self._json({"ok": True, "deleted": len(records)})
            record_id = path.rsplit("/", 1)[-1]
            kept = [r for r in records if r["id"] != record_id]
            if len(kept) == len(records):
                return self._error(404, "기록을 찾을 수 없습니다.")
            HISTORY[user] = kept
        self._json({"ok": True})

    # ---- GET ----
    def do_GET(self):
        url = urlparse(self.path)
        path = unquote(url.path)

        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/vtkjs.html")
            self.end_headers()
        elif path == "/api/health":
            self._json({
                "status": "ok", "checkpoint": CHECKPOINT,
                "rain_conditioned": True, "rain_range_mm": RAIN_RANGE,
                "time_conditioned": True, "time_range_s": TIME_RANGE,
                "default_time_s": DEFAULT_TIME_S, "image_size": 128, "device": "mock",
                "auth_enabled": REQUIRE_LOGIN, "db": "ok" if REQUIRE_LOGIN else "down",
            })
        elif path == "/api/samples":
            limit = int(parse_qs(url.query).get("limit", ["30"])[0])
            names = sorted(p.name for p in SAMPLES_DIR.glob("*.png")) if SAMPLES_DIR.is_dir() else []
            step = max(1, len(names) // max(limit, 1))
            self._json({"samples": names[::step][:limit]})
        elif path.startswith("/api/sample/"):
            target = (SAMPLES_DIR / path[len("/api/sample/"):]).resolve()
            if target.parent != SAMPLES_DIR.resolve() or not target.is_file():
                return self._error(404, "샘플을 찾을 수 없습니다.")
            self._file(target, "image/png")
        elif path == "/api/auth/me":
            user = self._user()
            self._json({"email": user}) if user else self._error(401, "토큰이 없거나 만료되었습니다.")
        elif path == "/api/history":
            user = self._history_user()
            if user:
                with LOCK:
                    self._json({"records": HISTORY.get(user, [])[:HISTORY_MAX]})
        elif path.startswith("/test_inputs/"):
            target = (TEST_INPUT_DIR / path[len("/test_inputs/"):]).resolve()
            if target.parent != TEST_INPUT_DIR.resolve() or not target.is_file():
                return self._error(404, "파일이 없습니다.")
            self._file(target, "application/octet-stream")
        else:
            # 프론트엔드 정적 파일 (vtkjs.html, style.css ...)
            target = (FRONTEND_DIR / path.lstrip("/")).resolve()
            if FRONTEND_DIR.resolve() not in target.parents or not target.is_file():
                return self._error(404, "없는 주소입니다.")
            ctype = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
                     ".js": "text/javascript; charset=utf-8", ".png": "image/png",
                     ".json": "application/json"}.get(target.suffix.lower(), "application/octet-stream")
            self._file(target, ctype)

    # ---- POST ----
    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_UPLOAD_BYTES + 1024 * 1024:
            return self._error(413, "파일이 25MB 를 초과합니다.")
        body = self.rfile.read(length)

        if path in ("/api/auth/signup", "/api/auth/login"):
            try:
                data = json.loads(body or b"{}")
                email, pw = str(data["email"]).strip().lower(), str(data["password"])
            except Exception:
                return self._error(422, "email, password 를 JSON 으로 보내주세요.")
            hashed = hashlib.sha256(pw.encode()).hexdigest()
            with LOCK:
                if path.endswith("signup"):
                    if email in USERS:
                        return self._error(400, "이미 가입된 이메일입니다.")
                    if len(pw) < 6:
                        return self._error(400, "비밀번호는 6자 이상이어야 합니다.")
                    USERS[email] = hashed
                elif USERS.get(email) != hashed:
                    return self._error(401, "이메일 또는 비밀번호가 올바르지 않습니다.")
                token = secrets.token_urlsafe(24)
                TOKENS[token] = email
            return self._json({"email": email, "token": token})

        if path == "/api/history":
            user = self._history_user()
            if not user:
                return
            data = json.loads(body or b"{}")
            rec = {
                "id": uuid.uuid4().hex,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "name": (data.get("name") or "").strip() or None,
                "fileName": data.get("fileName"),
                "params": data.get("params"),
                "drain": data.get("drain"),
                "checkpoint": data.get("checkpoint"),
                "meta": data.get("meta"),
                "info": data.get("info") or [],
                "imageLabel": data.get("imageLabel"),
                "thumbnail": data.get("thumbnail"),
            }
            with LOCK:
                HISTORY.setdefault(user, []).insert(0, rec)
            return self._json(rec)

        if path == "/api/predict":
            if REQUIRE_LOGIN and not self._user():
                return self._error(401, "로그인이 필요합니다.")
            ctype = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in ctype:
                return self._error(400, "multipart/form-data 로 보내주세요.")
            msg = BytesParser(policy=email_policy).parsebytes(
                b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + body)
            fields, file_raw, filename = {}, None, "upload"
            for part in msg.iter_parts():
                name = part.get_param("name", header="content-disposition")
                if part.get_filename():
                    filename, file_raw = part.get_filename(), part.get_payload(decode=True)
                else:
                    fields[name] = (part.get_payload(decode=True) or b"").decode()
            mode = fields.get("mode", "")
            if mode not in {"image", "terrain"}:
                return self._error(400, "mode 는 'image' 또는 'terrain' 이어야 합니다.")
            if not file_raw:
                return self._error(400, "빈 파일입니다.")
            try:
                time.sleep(0.4)   # 실제 추론처럼 잠깐 기다림 (버튼 '예측 중...' 확인용)
                result = predict(mode, file_raw, filename,
                                 float(fields.get("rain_mm", 50)), float(fields.get("time_s", DEFAULT_TIME_S)),
                                 float(fields.get("dx", DEFAULT_DX_M)))
            except Exception as exc:  # noqa: BLE001
                return self._error(422, f"처리할 수 없는 입력입니다: {exc}")
            return self._json(result)

        self._error(404, "없는 주소입니다.")


def main():
    global REQUIRE_LOGIN
    ap = argparse.ArgumentParser(description="유체이탈 테스트용 가짜 AI 서버")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--require-login", action="store_true", help="로그인해야 예측 가능 (진짜 서버 DB 연결 상태 흉내)")
    ap.add_argument("--no-browser", action="store_true", help="브라우저 자동 열기 끄기")
    args = ap.parse_args()
    REQUIRE_LOGIN = args.require_login

    make_test_inputs()
    try:
        httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError:
        print(f"\n[오류] {args.host}:{args.port} 포트를 이미 다른 프로그램이 쓰고 있습니다.")
        print("       진짜 AI 서버가 켜져 있다면 끄거나,  --port 8100  처럼 다른 포트로 실행하세요.")
        print("       (다른 포트면 브라우저 주소에 ?api=http://127.0.0.1:8100 을 붙여야 합니다)\n")
        sys.exit(1)

    base = f"http://{args.host}:{args.port}"
    page = f"{base}/vtkjs.html" + ("" if args.port == 8000 and args.host == "127.0.0.1" else f"?api={base}")
    print("=" * 64)
    print(" 유체이탈 테스트용 가짜 AI 서버")
    print(f"  화면       : {page}")
    print(f"  샘플 등고선: {SAMPLES_DIR}  ({len(list(SAMPLES_DIR.glob('*.png'))) if SAMPLES_DIR.is_dir() else 0}장)")
    print(f"  고도 격자  : {TEST_INPUT_DIR}  (등고선 데이터 모드 시험용)")
    print(f"  로그인 필수: {'예' if REQUIRE_LOGIN else '아니오'}  (가입 정보는 서버를 끄면 사라짐)")
    print("  끄기       : Ctrl+C")
    print("=" * 64)
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(page)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")


if __name__ == "__main__":
    main()
