"""유체이탈 동작 흐름도 SVG 생성: ① 학습 데이터 만들기 → ② 학습 과정 → ③ 작동(추론).

사용: python make_flowchart.py 출력.svg
"""
import sys
from html import escape

W, H = 1800, 1240
BG, PANEL, BORDER, TEXT, MUTED = "#0f141a", "#18202a", "#2a3542", "#e6eaef", "#8592a3"
BLUE, TEAL, PURPLE, ORANGE, RED = "#3398e0", "#2bb39b", "#9b7be0", "#e0a33b", "#e5687a"
FONT = "'Malgun Gothic','Segoe UI',sans-serif"

out = []


def rect(x, y, w, h, fill=PANEL, stroke=BORDER, rx=10, sw=1.2, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"{da}/>')


def text(x, y, s, size=12, fill=TEXT, weight=400, anchor="start"):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
               f'text-anchor="{anchor}">{escape(s)}</text>')


def arrow(points, color=MUTED, sw=1.6, dash="", label=None, lpos=None):
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{da} '
               f'stroke-linejoin="round" marker-end="url(#a-{color[1:]})"/>')
    if label:
        lx, ly = lpos
        tw = len(label) * 7.2 + 16
        rect(lx - tw / 2, ly - 12, tw, 22, BG, BORDER, 11, 1)
        text(lx, ly + 4, label, 11, MUTED, anchor="middle")


def node(x, y, w, h, title, lines=(), color=BLUE, highlight=False):
    rect(x, y, w, h, "#15293a" if highlight else PANEL, color if highlight else BORDER, 10,
         2 if highlight else 1.2)
    out.append(f'<rect x="{x}" y="{y + 10}" width="4" height="{h - 20}" rx="2" fill="{color}"/>')
    text(x + 16, y + 26, title, 14, TEXT, 700)
    for i, ln in enumerate(lines):
        text(x + 16, y + 48 + i * 18, ln, 12, MUTED)
    return (x, y, w, h)


def lane(y, h, num, name, color, desc):
    rect(20, y, W - 40, h, "none", BORDER, 14, 1, "4 6")
    # 손그림의 마름모 라벨
    cx, cy = 92, y + 40
    out.append(f'<polygon points="{cx - 62},{cy} {cx},{cy - 26} {cx + 62},{cy} {cx},{cy + 26}" '
               f'fill="{BG}" stroke="{color}" stroke-width="2"/>')
    text(cx, cy + 5, f"{num} {name}", 14, color, 700, "anchor")
    out[-1] = out[-1].replace('text-anchor="anchor"', 'text-anchor="middle"')
    text(170, y + 45, desc, 13, MUTED)


def mid_r(n):  # 노드 오른쪽 가운데
    x, y, w, h = n
    return (x + w, y + h / 2)


def mid_l(n):
    x, y, w, h = n
    return (x, y + h / 2)


# ------------------------------------------------------------------ 머리말
out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
text(40, 52, "유체이탈 동작 흐름도", 26, TEXT, 700)
text(40, 80, "학습 데이터를 만들고 → U-Net을 학습시키고 → 웹에서 예측하기까지", 14, MUTED)
rect(1330, 28, 430, 64, PANEL, BORDER, 10)
text(1346, 52, "PyTorch  모델 정의 · 학습 · 추론을 맡는 딥러닝 프레임워크", 12, TEXT)
text(1346, 74, "FastAPI  예측 요청을 받아 모델을 실행하는 파이썬 웹 서버", 12, TEXT)

# ------------------------------------------------------------------ ① 데이터
LA_Y, LA_H = 110, 270
lane(LA_Y, LA_H, "①", "학습 데이터", ORANGE, "실제 지형에 물리 시뮬레이션을 돌려 '정답'을 만든다 — 한 건에 10~20분")
NW, GAP = 202, 26
ax0, ay = 44, LA_Y + 110
data_nodes = [
    ("국가기본도 등고선", ["서울 · 부산 · 강원", "실제 지형 586종"]),
    ("고도 격자 추출", ["96×96 격자", "dx 10.4m (1km×1km)"]),
    ("OpenFOAM 시뮬레이션", ["interFoam (VOF 유체)", "강우 20~80mm · 120초"]),
    ("수심 결과", ["depth.npy (m)", "시점 6개 저장"]),
    ("이미지 쌍 렌더링", ["입력: 등고선 20단계 채색", "정답: 파란 수심맵(Blues)"]),
    ("데이터 증강", ["회전·뒤집기 D4 8배", "총 48,528쌍"]),
    ("지형 단위 분리", ["학습 85% / 검증 15%", "같은 지형은 한쪽에만"]),
]
prev = None
for i, (t, ls) in enumerate(data_nodes):
    n = node(ax0 + i * (NW + GAP), ay, NW, 96, t, ls, ORANGE, highlight=(i == 2))
    if prev:
        arrow([mid_r(prev), (n[0] - 2, mid_l(n)[1])], ORANGE)
    prev = n
last_data = prev

# ------------------------------------------------------------------ ② 학습
LB_Y, LB_H = 410, 410
lane(LB_Y, LB_H, "②", "학습 과정", PURPLE, "예측과 정답의 차이(손실)를 줄이도록 가중치를 반복 조정 — PyTorch")

in_img = node(44, 490, 210, 96, "등고선 이미지", ["128×128 × RGB 3채널", "모델의 입력"], BLUE)
in_cond = node(44, 660, 210, 96, "조건 벡터", ["강우량 → 0~1 정규화", "경과시간 → 0~1 정규화"], TEAL)

# 데이터 → 학습 입력
DX = last_data[0] + NW / 2
arrow([(DX, last_data[1] + 96), (DX, 395), (149, 395), (149, 488)], ORANGE, dash="6 5",
      label="학습 쌍 공급 (배치 16) — 입력은 모델로", lpos=(800, 395))
arrow([(DX, 395), (1630, 395), (1630, 438)], ORANGE, dash="6 5")
text(1640, 420, "정답은 손실 계산으로", 11, ORANGE)

# U-Net 상자 (작은 V자 모식도만)
UX, UY, UW, UH = 300, 470, 620, 320
rect(UX, UY, UW, UH, PANEL, PURPLE, 14, 2)
text(UX + 20, UY + 30, "U-Net 생성자", 16, PURPLE, 700)
text(UX + 128, UY + 30, "pix2pix형 · 파라미터 10.5M · 128→1 까지 7단 축소 후 복원", 12, MUTED)
text(UX + 20, UY + 52, "파랑 = 줄이며 특징 추출 · 보라 = 키우며 복원 · 점선 = skip connection(같은 크기끼리 복사)", 11, MUTED)

chans = [3, 32, 64, 128, 256, 256, 256]
STEP_X, STEP_Y = 30, 17
ex0, yc0 = UX + 60, UY + 110


def bar_h(i):
    return 12 + 7 * (7 - i)


def bar_w(c):
    return 6 + c / 256 * 8


enc, dec = [], []
for i in range(7):
    yc = yc0 + i * STEP_Y
    h = bar_h(i)
    enc.append((ex0 + i * STEP_X, yc, bar_w(chans[i]), h))
    wd = bar_w(chans[i] if i else 3)
    dec.append((UX + UW - 60 - i * STEP_X - wd, yc, wd, h))

# 병목 (1×1, FiLM 적용 지점)
bott = (UX + UW / 2 - 9, yc0 + 7 * STEP_Y, 18, bar_h(7))

for x, yc, w, h in enc:
    rect(x, yc - h / 2, w, h, "#2a3a4c", BLUE, 2, 1)
for x, yc, w, h in dec:
    rect(x, yc - h / 2, w, h, "#2c2a45", PURPLE, 2, 1)
x, yc, w, h = bott
rect(x, yc - h / 2, w, h, "#3a2f1d", ORANGE, 2, 1.5)
text(x + w + 8, yc + 4, "병목", 11, ORANGE, 700)

for i in range(6):
    a, b = enc[i], enc[i + 1]
    arrow([(a[0] + a[2], a[1] + a[3] / 2 - 4), (b[0] - 2, b[1])], BLUE, 1.2)
arrow([(enc[6][0] + enc[6][2], enc[6][1] + 4), (bott[0] - 2, bott[1])], BLUE, 1.2)
arrow([(bott[0] + bott[2], bott[1]), (dec[6][0] - 2, dec[6][1] + 4)], PURPLE, 1.2)
for i in range(6, 0, -1):
    a, b = dec[i], dec[i - 1]
    arrow([(a[0] + a[2], a[1]), (b[0] - 2, b[1] + b[3] / 2 - 4)], PURPLE, 1.2)
for i in range(1, 7):
    a, b = enc[i], dec[i]
    y = a[1] - a[3] / 2 + 5
    arrow([(a[0] + a[2] + 2, y), (b[0] - 2, y)], "#5f6b7a", 1, "3 4")

# FiLM
FX, FY, FW, FH = UX + UW / 2 - 140, UY + UH - 72, 280, 56
rect(FX, FY, FW, FH, "#1d2b2a", TEAL, 10, 1.8)
text(FX + FW / 2, FY + 22, "FiLM 조건 주입", 14, TEAL, 700, "middle")
text(FX + FW / 2, FY + 42, "조건 → 채널별 γ, β  ·  병목 특징 × (1+γ) + β", 12, MUTED, anchor="middle")
arrow([(FX + FW / 2, FY), (FX + FW / 2, bott[1] + bott[3] / 2 + 3)], TEAL, 1.6)

# 입력 → U-Net
arrow([mid_r(in_img), (UX + 20, mid_r(in_img)[1]), (UX + 20, enc[0][1]), (enc[0][0] - 3, enc[0][1])], BLUE)
arrow([mid_r(in_cond), (FX - 3, FY + FH / 2)], TEAL)

# 출력 / 손실 / 역전파
pred = node(980, 500, 220, 86, "예측 수심 이미지", ["128×128 × 3", "파란색 진할수록 깊음"], PURPLE)
truth = node(1500, 440, 260, 86, "정답 (OpenFOAM)", ["같은 지형·강우·시점의", "실제 시뮬레이션 수심맵"], ORANGE)
loss = node(1500, 560, 260, 104, "손실함수 비교", ["젖은 픽셀 가중 L1", "물 있는 곳 오차 × 8배", "λ=100 · GAN 없이 학습"], RED,
            highlight=True)
back = node(1230, 690, 230, 86, "역전파 · 가중치 갱신", ["Adam lr 0.0002", "β1 0.5 · 30 epoch"], RED)
best = node(1500, 690, 260, 104, "검증 · 저장", ["2 epoch마다 검증셋 L1 측정", "가장 좋을 때 best.pt 저장", "10번 개선 없으면 조기 종료"],
            PURPLE)

arrow([(dec[0][0] + dec[0][2] + 2, dec[0][1]), (950, dec[0][1]), (950, 543), (978, 543)], PURPLE)
arrow([mid_r(pred), (1470, 543), (1470, 600), (1498, 600)], PURPLE)
arrow([(1630, 526), (1630, 558)], ORANGE)
arrow([(1500, 640), (1480, 640), (1480, 733), (1462, 733)], RED)
arrow([(1230, 733), (922, 733)], RED, label="가중치 수정 → 다시 예측 (반복)", lpos=(1076, 760))
arrow([(1630, 664), (1630, 688)], RED)

# ------------------------------------------------------------------ ③ 작동
LC_Y, LC_H = 850, 360
lane(LC_Y, LC_H, "③", "작동 (추론)", BLUE, "학습이 끝난 best.pt로 사용자 요청을 바로 예측 — 한 건 수백 ms")
CY = LC_Y + 120
CH = 150
run_nodes = [
    ("사용자 화면", ["vtkjs.html", "파일 업로드 또는 샘플", "강우·경과시간 슬라이더"], BLUE),
    ("POST /api/predict", ["FormData 전송", "mode · file · rain_mm", "time_s · dx (+토큰)"], BLUE),
    ("입력 전처리", ["image: 그림 그대로", "terrain: 고도 격자 읽기", "→ 학습과 같은 등고선 렌더"], TEAL),
    ("U-Net 추론", ["best.pt 불러오기", "등고선 → 128×128", "강우·시간 → FiLM"], PURPLE),
    ("후처리", ["등고선 + 예측 오버레이", "terrain: 최대 유출점 =", "배수구 후보 + 분석 지도"], TEAL),
    ("JSON 응답", ["PNG 4종 (base64)", "drain_candidate 좌표", "meta · notes"], BLUE),
    ("결과 표시", ["입력·배수맵·오버레이", "나란히 + PNG 저장", "로그인 시 기록 저장"], BLUE),
]
prev = None
run = []
for i, (t, ls, c) in enumerate(run_nodes):
    n = node(ax0 + i * (NW + GAP), CY, NW, CH - 30, t, ls, c, highlight=(i == 3))
    run.append(n)
    if prev:
        arrow([mid_r(prev), (n[0] - 2, mid_l(n)[1])], c if i != 3 else PURPLE)
    prev = n

# best.pt → 추론
u = run[3]
arrow([(1630, 794), (1630, 835), (u[0] + NW / 2, 835), (u[0] + NW / 2, u[1] - 2)], PURPLE, 1.8, "7 5",
      label="학습된 가중치 best.pt 전달 (checkpoints_p2_wet8)", lpos=(1240, 835))

# 서버 경계 표시
sx0 = run[1][0] - 12
sx1 = run[5][0] + NW + 12
rect(sx0, CY - 36, sx1 - sx0, CH + 10, "none", TEAL, 12, 1.2, "3 5")
text(sx0 + 12, CY - 16, "AI 모델 서버 · FastAPI :8000 (terrainFlowSim/webapp)", 12, TEAL, 700)
text(ax0, CY - 16, "브라우저", 12, BLUE, 700)
text(run[6][0], CY - 16, "브라우저", 12, BLUE, 700)

# 하단 메모
notes = [
    "· 경과시간이 짧을수록 물이 많다 (비가 초반에 내리고 빠지는 시뮬레이션) → 기본값 18초",
    "· 학습 범위(강우 20~80mm, 0~120초) 밖 값은 경계값으로 잘라서 모델에 넣는다",
    "· MySQL이 연결돼 있으면 로그인 토큰이 있어야 예측 가능, 없으면 인증 생략",
]
for i, s in enumerate(notes):
    text(ax0, CY + CH + 16 + i * 20, s, 12, MUTED)
text(1000, CY + CH + 16, "검증 성능 (학습에 안 쓴 지형 87종)", 12, TEXT, 700)
text(1000, CY + CH + 36, "평균 수심 오차 0.0115m · 젖은영역 IoU@1cm 0.69 · 상관 r 0.68", 12, MUTED)
text(1000, CY + CH + 56, "강우가 많을 때 더 깊게 예측한 비율 98.8%", 12, MUTED)

# 화살표 머리 (색별)
colors = {BLUE, TEAL, PURPLE, ORANGE, RED, MUTED, "#5f6b7a"}
defs = ["<defs>"] + [
    f'<marker id="a-{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
    f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in colors
] + ["</defs>"]

svg = ([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}">'] + defs + out + ["</svg>"])
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
