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

## 기록을 백엔드 서버에 저장하게 되면 바꿀 부분

지금 분석 기록은 **브라우저 localStorage** 에만 저장됩니다(사용자별 키 `yuche_history_{이메일}`, 최근 20건).
그래서 다른 PC·브라우저에서는 기록이 안 보입니다. 서버 저장으로 바꿀 때 `yuche_frontend/vtkjs.html` 에서 고칠 곳:

| 함수 | 지금 | 바꿀 내용 |
|---|---|---|
| `loadHistory()` | localStorage 읽기 | `GET /api/history` (헤더 `Authorization: Bearer 토큰`) |
| `saveRecord(record)` | 맨 앞에 추가 후 저장 | `POST /api/history` |
| `updateRecord(id, changes)` | 이름 변경 저장 | `PATCH /api/history/{id}` (`{ name }`) |
| `deleteRecord(id)` / `clearHistory()` | 목록에서 삭제 | `DELETE /api/history/{id}` / `DELETE /api/history` |
| `historyKey()` · `writeHistory()` | localStorage 키·용량 처리 | 필요 없어짐 (삭제) |

- 서버 호출은 비동기라서 `loadHistory()` 를 쓰는 `renderHistory()`, `showRecord()`, `showDetail()`, `startRename()` 도 `async/await` 로 바꿔야 합니다.
- 결과 그림(`thumbnail`)은 지금 base64 JPEG 문자열로 저장합니다(`makeThumbnail()`). 서버에서는 파일로 저장하고 URL만 돌려주는 편이 좋습니다.
- 기록 하나에 저장하는 값(= DB 테이블 칼럼 후보):

  | 필드 | 내용 |
  |---|---|
  | `id`, `createdAt` | 기록 ID, 저장 시각 (ISO) |
  | `name` | 사용자가 정한 이름. `null` 이면 화면에 '날짜 시간' 표시 |
  | `fileName` | 입력 파일 이름 |
  | `params` | `{ mode, rain_mm, time_s, dx }` |
  | `drain` | 배수구 후보 좌표 `{ x, y }` 또는 `null` |
  | `checkpoint`, `meta`, `info` | 사용한 모델, 서버 meta, 결과 안내문 |
  | `imageLabel`, `thumbnail` | 대표 그림 이름, 그림 |

- 로그인 토큰은 이미 AI 서버의 `/api/auth/login` 에서 받아 `localStorage['yuche_token']` 에 저장하고 있으니 그대로 쓰면 됩니다. 기록 API를 다른 서버에 만들면 그 서버 주소용 상수를 `DEFAULT_API` 옆에 하나 더 추가하세요.
