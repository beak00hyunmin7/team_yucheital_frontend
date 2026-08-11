# 데이터셋 구성 방법 (나중에 채워 넣을 부분)

```
data/
├── contours/   # 입력: 등고선 이미지들
│   ├── 0001.png
│   ├── 0002.png
│   └── ...
└── flow/       # 타깃: 배수 시뮬레이션 결과 이미지 (첨부하신 파란 정사각형 같은 이미지)
    ├── 0001.png
    ├── 0002.png
    └── ...
```

- `contours/`와 `flow/`에 **같은 파일명**으로 입력-정답 이미지 쌍을 넣으면 됩니다.
- 두 폴더의 파일명이 정확히 일치하는 것만 학습에 쓰입니다 (`src/datasets/contour_flow_dataset.py`).
- 이미지 크기는 로딩 시 `configs/config.yaml`의 `image_size`(기본 256)로 자동 리사이즈되므로 원본 크기는 자유롭습니다.
- 데이터가 준비되면 `python -m src.train --config configs/config.yaml`로 바로 학습을 시작할 수 있습니다.
