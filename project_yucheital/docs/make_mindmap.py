"""유체이탈 시스템 구조 마인드맵 SVG 생성."""
import sys
from html import escape

W, H = 1600, 1210
BG, PANEL, BORDER, TEXT, MUTED = "#0f141a", "#18202a", "#2a3542", "#e6eaef", "#8592a3"
FONT = "'Malgun Gothic','Segoe UI',sans-serif"

CENTER = (800, 470)

BRANCHES = [
    {   # 왼쪽 위
        "name": "프론트엔드", "sub": "yuche_frontend · vtkjs.html", "color": "#3398e0",
        "pos": (520, 240), "side": "left",
        "leaves": [
            ("화면 구성", "단일 페이지 · 다크/라이트 토큰(style.css)"),
            ("1. 입력", "등고선 이미지 / 고도 격자 · 샘플 갤러리"),
            ("2. 조건", "강우 20–80mm · 경과 0–120초 · dx"),
            ("3. 결과", "입력 등고선 · 예측 배수맵 · 오버레이"),
            ("기록 · 로그인", "localStorage 최근 20건 · Bearer 토큰"),
        ],
    },
    {   # 오른쪽 위
        "name": "AI 모델 서버", "sub": "terrainFlowSim/webapp · FastAPI :8000", "color": "#2bb39b",
        "pos": (1080, 240), "side": "right",
        "leaves": [
            ("GET /api/health", "체크포인트 · CPU/CUDA · 학습 범위"),
            ("GET /api/samples", "지역별 샘플 등고선 PNG 목록"),
            ("POST /api/predict", "mode·file·rain_mm·time_s·dx → PNG 4종"),
            ("/api/auth/*", "login · signup · me (MySQL 있을 때만)"),
            ("/api/testset · testcase", "OpenFOAM 정답과 나란히 검증"),
        ],
    },
    {   # 오른쪽 아래
        "name": "AI 모델", "sub": "team_yucheital_ai_model", "color": "#9b7be0",
        "pos": (1080, 710), "side": "right",
        "leaves": [
            ("U-Net 생성자", "10.5M 파라미터 · 128×128 입력"),
            ("FiLM 조건 주입", "강우량 + 경과시간 → 병목층"),
            ("체크포인트", "checkpoints_p2_wet8/best.pt"),
            ("학습 데이터", "OpenFOAM interFoam · 586지형 · 48,528쌍"),
            ("성능 (미학습 지형)", "MAE 0.0115m · IoU@1cm 0.69 · r 0.68"),
        ],
    },
    {   # 왼쪽 아래
        "name": "백엔드 · DB", "sub": "team_yucheital_backend", "color": "#e0a33b",
        "pos": (520, 710), "side": "left",
        "leaves": [
            ("FastAPI + MySQL", "Docker compose · Swagger /docs"),
            ("AI_BACKEND", "unet 기본 · 실패 시 D8 흐름누적 폴백"),
            ("자동 검증", "규칙 · D8 모의배수 · 최대 2회 재분석"),
            ("저장", "입력·워터맵·좌표 → 재학습 대기 등록"),
            ("yuche_backend (로컬)", "/signup · /login · bcrypt · users 테이블"),
        ],
    },
]

FLOW = [
    ("사용자 입력", "등고선 + 강우·시간"),
    ("POST /api/predict", "FormData 전송"),
    ("전처리", "고도 격자 → 등고선 렌더"),
    ("U-Net 추론", "FiLM 조건 반영"),
    ("응답", "base64 PNG + 배수구 좌표"),
    ("화면 · 기록", "3분할 결과 · 썸네일 저장"),
]

BW, BH = 250, 72          # 가지 노드
LW, LH, LGAP = 300, 60, 16  # 잎 노드


def rect(x, y, w, h, fill, stroke, rx=10, sw=1.5, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def text(x, y, s, size, fill, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')


def curve(x1, y1, x2, y2, color, sw=2, dash=""):
    mx = (x1 + x2) / 2
    d = f"M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{da}/>'


out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="{FONT}">',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>',
       text(40, 52, "유체이탈 시스템 구조", 26, TEXT, 700),
       text(40, 80, "프론트엔드 · AI 모델 서버 · 백엔드가 어떻게 연결되는지 한눈에 보기", 14, MUTED)]

cx, cy = CENTER
edges, nodes = [], []

for b in BRANCHES:
    bx, by = b["pos"]
    col = b["color"]
    left = b["side"] == "left"
    # 중심 -> 가지
    sx = cx - 120 if bx < cx else cx + 120
    ex = bx + BW / 2 if bx < cx else bx - BW / 2
    edges.append(curve(sx, cy, ex, by, col, 3))

    nodes.append(rect(bx - BW / 2, by - BH / 2, BW, BH, PANEL, col, 12, 2.5))
    nodes.append(text(bx, by - 4, b["name"], 18, col, 700, "middle"))
    nodes.append(text(bx, by + 20, b["sub"], 12, MUTED, 400, "middle"))

    n = len(b["leaves"])
    total = n * LH + (n - 1) * LGAP
    top = by - total / 2
    lx = 40 if left else W - 40 - LW
    for i, (title, detail) in enumerate(b["leaves"]):
        ly = top + i * (LH + LGAP)
        lcy = ly + LH / 2
        if left:
            edges.append(curve(bx - BW / 2, by, lx + LW, lcy, col, 1.5))
        else:
            edges.append(curve(bx + BW / 2, by, lx, lcy, col, 1.5))
        nodes.append(rect(lx, ly, LW, LH, PANEL, BORDER, 8, 1))
        nodes.append(f'<rect x="{lx}" y="{ly + 10}" width="4" height="{LH - 20}" rx="2" fill="{col}"/>')
        nodes.append(text(lx + 16, ly + 25, title, 14, TEXT, 600))
        nodes.append(text(lx + 16, ly + 45, detail, 12, MUTED))

# 가지 사이 실제 호출 관계 (점선)
fe, srv, model, be = (b["pos"] for b in BRANCHES)
links = [
    ((fe[0] + BW / 2 - 20, fe[1] - BH / 2), (srv[0] - BW / 2 + 20, srv[1] - BH / 2), "HTTP fetch · JSON", -70),
    ((srv[0] + 30, srv[1] + BH / 2), (model[0] + 30, model[1] - BH / 2), "predict_from_image()", 0),
    ((be[0] + BW / 2 - 20, be[1] + BH / 2), (model[0] - BW / 2 + 20, model[1] + BH / 2), "unet_infer 사본 (deploy_package)", 70),
]
for (x1, y1), (x2, y2), label, bend in links:
    if bend:
        my = y1 + bend
        edges.append(f'<path d="M{x1},{y1} C{x1},{my} {x2},{my} {x2},{y2}" fill="none" stroke="{MUTED}" '
                     f'stroke-width="1.5" stroke-dasharray="6 6" marker-end="url(#arr)"/>')
        lxm, lym = (x1 + x2) / 2, y1 + bend * 0.75
    else:
        edges.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{MUTED}" stroke-width="1.5" '
                     f'stroke-dasharray="6 6" marker-end="url(#arr)"/>')
        lxm, lym = x1 + 12, (y1 + y2) / 2
    tw = len(label) * 7.4 + 16
    ax = lxm - tw / 2 if bend else lxm
    nodes.append(rect(ax, lym - 13, tw, 24, BG, BORDER, 12, 1))
    nodes.append(text(ax + tw / 2, lym + 4, label, 12, MUTED, 400, "middle"))

# 중심 노드
nodes.append(rect(cx - 120, cy - 52, 240, 104, "#15293a", "#3398e0", 16, 2.5))
nodes.append(text(cx, cy - 8, "유체이탈", 28, TEXT, 700, "middle"))
nodes.append(text(cx, cy + 20, "등고선 → 침수 수심 예측", 14, "#a6cbec", 400, "middle"))
nodes.append(text(cx, cy + 40, "OpenFOAM 10~20분 → 수백 ms", 12, MUTED, 400, "middle"))

# 하단: 요청 한 번의 흐름
fy = 950
out_flow = [rect(40, fy - 40, W - 80, 170, PANEL, BORDER, 12, 1),
            text(64, fy - 10, "예측 요청 한 번의 흐름", 16, TEXT, 700)]
n = len(FLOW)
gap = 24
fw = (W - 80 - 48 - gap * (n - 1)) / n
for i, (t, d) in enumerate(FLOW):
    x = 64 + i * (fw + gap)
    y = fy + 16
    hl = t == "U-Net 추론"
    out_flow.append(rect(x, y, fw, 72, "#15293a" if hl else BG, "#9b7be0" if hl else BORDER, 8, 1.5 if hl else 1))
    out_flow.append(f'<circle cx="{x + 20}" cy="{y + 22}" r="11" fill="#3398e0"/>')
    out_flow.append(text(x + 20, y + 27, str(i + 1), 12, "#ffffff", 700, "middle"))
    out_flow.append(text(x + 38, y + 27, t, 14, TEXT, 600))
    out_flow.append(text(x + 16, y + 54, d, 12, MUTED))
    if i < n - 1:
        ax = x + fw + 4
        out_flow.append(f'<path d="M{ax},{y + 36} L{ax + gap - 8},{y + 36}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr)"/>')

out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
           f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
out += ['<g transform="translate(0,70)">'] + edges + nodes + out_flow + ['</g>', '</svg>']

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
