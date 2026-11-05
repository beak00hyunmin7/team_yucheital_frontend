# 유체이탈 프론트엔드

## 실행 방법

**준비물**: Python 3.10 이상 (설치할 때 "Add python.exe to PATH" 체크)

```powershell
git clone https://github.com/beak00hyunmin7/team_yucheital_frontend.git
```

1. `project_yucheital/run_test_server.bat` 더블클릭
2. 브라우저가 `http://127.0.0.1:8000/vtkjs.html` 로 열리고, 오른쪽 위가 🟢 이면 성공
3. 끌 때는 검은 창에서 `Ctrl+C`

- 이건 **테스트용 가짜 서버**(`project_yucheital/dev_server/mock_server.py`)라서 예측 그림은 진짜 AI 결과가 아닙니다. 화면 기능 확인용입니다.
- **진짜 AI 서버**를 쓰려면 AI 저장소의 `terrainFlowSim/webapp/run_windows.bat` 을 실행하고(체크포인트 `best.pt` 필요), 테스트 서버는 끈 채로 `yuche_frontend/vtkjs.html` 을 열면 됩니다.
- 서버 주소는 `yuche_frontend/vtkjs.html` 의 `DEFAULT_API` 한 줄에서 바꿉니다. 파일을 고치지 않으려면 주소 뒤에 `?api=http://IP:포트` 를 붙여도 됩니다.

## 분석 기록 저장

분석 기록은 AI 서버의 `/api/history` 에 저장됩니다(MySQL + 썸네일 파일). 로그인한 사용자 본인 기록만 보이고, 다른 PC·브라우저에서도 같은 기록이 보입니다. 목록은 최신순 최대 50건입니다.

| 동작 | API |
|---|---|
| 목록 | `GET /api/history` |
| 저장 (예측 완료 시 자동) | `POST /api/history` |
| 이름 변경 | `PATCH /api/history/{id}` (`{ name }`) |
| 삭제 / 전체 삭제 | `DELETE /api/history/{id}` / `DELETE /api/history` |

- 모든 요청에 `Authorization: Bearer 토큰` 헤더가 필요합니다. 토큰은 `/api/auth/login` 에서 받아 `localStorage['yuche_token']` 에 저장합니다.
- 비로그인 상태나 DB 가 끊긴 상태에서는 기록이 저장되지 않습니다. 저장에 실패하면 결과 안내에 한 줄로 표시됩니다.
- 예전 localStorage 기록(`yuche_history_{이메일}`)은 서버로 옮기지 않았고, 화면에도 보이지 않습니다.
- 테스트 서버도 같은 API 를 제공하지만 기록을 메모리에만 두므로 서버를 끄면 사라집니다.

## 배수구 후보 위치

`POST /api/predict` 응답의 `drain_candidate.image` `{ x, y }` 는 그림 왼쪽 위 기준 0~1 비율입니다. 예측 배수맵과 오버레이 위에 빨간 원으로 표시하고, 기록의 `drain` 에도 이 값을 저장합니다.
