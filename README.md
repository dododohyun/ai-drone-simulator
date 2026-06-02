# DroneBlocks Tello Simulator (Python) — 의자 착륙 프로젝트

이 저장소는 **DroneBlocks Tello 시뮬레이터**를 Python 으로 제어하고,
같은 코드를 **실제 Tello / Tello EDU** 로 그대로 옮겨 실행하기 위한 환경입니다.

핵심 목표: 시뮬레이터에서 비행 경로를 검증한 뒤, 동일한 시퀀스를 실기로 재현해
"드론을 의자 좌석 중앙에 착륙시키는" 미션을 수행합니다.

---

## 1. 프로젝트 구조

```
.
├── README.md                          # ← 이 문서
├── src/DroneBlocksTelloSimulator/     # 라이브러리 본체 (시뮬레이터 + 실기 공용)
│   ├── DroneBlocksSimulatorContextManager.py
│   ├── tello.py                       # 실제 Tello SDK 래퍼 (UDP 192.168.10.1:8889)
│   └── drone.py
├── examples/
│   ├── test-context-mgr.py            # 시뮬레이터 동작 확인용 샘플
│   ├── chair-landing.py               # 의자 착륙 시퀀스 (시뮬레이터)
│   └── chair-landing-real.py          # 의자 착륙 시퀀스 (실제 Tello EDU)
└── venv/                              # 가상환경 (선택)
```

---

## 2. 환경 구축

### 2.1 가상환경 생성 및 활성화

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\activate
```

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.2 패키지 설치

```
pip install DroneBlocksTelloSimulator
```

---

## 3. 시뮬레이터 사용법

### 3.1 시뮬레이터 접속

[DroneBlocks Simulator](http://coding-sim.droneblocks.io/) 에 접속합니다.

Chrome 에서 **"Allow Insecure Content"** 설정이 필요합니다 (보안 위험 없음, 이 도메인에만 적용):
1. 주소창 왼쪽 자물쇠 아이콘 클릭
2. **Site settings**
3. 하단의 **Insecure content** 항목을 **Block → Allow** 로 변경
4. 탭을 닫고 시뮬레이터 새로고침

### 3.2 시뮬레이터 키 발급

좌상단 **"Get Drone Simulator Key"** 버튼을 눌러 키를 복사합니다.
키는 `examples/chair-landing.py` 상단의 `sim_key` 변수에 붙여 넣습니다.

### 3.3 시뮬레이터 실행

```powershell
python examples/chair-landing.py
```

`examples/chair-landing.py` 는 다음 시퀀스를 단계별로 실행합니다 (단위: cm):

| 단계 | 동작 | 거리 | 비고 |
|------|------|------|------|
| 1 | takeoff | - | 이륙 |
| 2 | fly_up | (주석 처리) | 필요 시 활성화 |
| 3 | fly_forward | 40 | 의자 앞쪽으로 전진 |
| 4 | fly_left | 20 | 왼쪽으로 정렬 |
| 5 | fly_forward | 20 | 앞으로 미세 전진 |
| 6 | fly_right | 20 | 오른쪽으로 정렬 |
| 7 | fly_backward | 10 | 의자 중심 좌석 위로 후진 |
| 8 | land | - | 의자 중심에 착륙 |

---

## 4. 실제 Tello EDU 사용법

### 4.1 사전 준비

1. PC의 Wi-Fi 를 **TELLO-XXXXXX** 네트워크에 연결
2. 드론 주변 안전 공간 확보 (천장/벽/사람 주의)
3. 배터리 **30% 이상** 권장

### 4.2 실행

```powershell
python examples/chair-landing-real.py
```

`examples/chair-landing-real.py` 는 시뮬레이터 버전과 동일한 순서를 실기로 수행합니다.
다른 점은 단 4가지뿐입니다:

| 시뮬레이터 (`chair-landing.py`) | 실제 Tello (`chair-landing-real.py`) |
|---|---|
| `DroneBlocksSimulatorContextManager(sim_key)` 사용 | `Tello()` 직접 생성 |
| `with` 블록이 takeoff/land 관리 | `tello.connect()` 명시적 호출 |
| 배터리 확인 없음 | `print(tello.get_battery())` 로 사전 확인 |
| 자동 소켓 정리 | 마지막에 `tello.end()` 호출 |

### 4.3 ⚠ 실기 사용 시 주의

- Tello SDK 의 `move` 명령은 **20 ~ 500 cm 정수**만 허용합니다.
- 시뮬레이터에서 통과한 거리값 (예: 5cm, 2.5cm) 은 실제 드론이 **명령 자체를 거부**합니다.
- 실기 테스트 전에 모든 거리값을 **20 이상 정수**로 조정하세요.

---

## 5. 사용 가능한 명령어

시뮬레이터와 실기 모두에서 동작하는 공통 명령입니다.

```python
drone.takeoff()
drone.fly_forward(20, 'cm')
drone.fly_backward(20, 'cm')
drone.fly_left(20, 'cm')
drone.fly_right(20, 'cm')
drone.fly_up(20, 'cm')
drone.fly_down(20, 'cm')
drone.fly_to_xyz(10, 20, 30, 'cm')
drone.fly_curve(25, 25, 0, 0, 50, 0, 'cm')
drone.flip_forward()
drone.flip_backward()
drone.flip_left()
drone.flip_right()
drone.land()
```

실기 전용 추가 명령 (`Tello` 클래스 직접 사용 시):

```python
tello = Tello()
tello.connect()                # SDK 모드 진입
tello.get_battery()            # 배터리 잔량 (%)
tello.set_speed(40)            # 이동 속도 (10~100 cm/s)
tello.emergency()              # 비상 정지 (모터 즉시 OFF)
tello.end()                    # 소켓 정리
```

---

## 6. 단위 (Units)

`fly_*` 계열 함수의 두 번째 인자는 단위 문자열입니다:

- `'cm'` — 센티미터 (현재 이 프로젝트 기준)
- `'in'` — 인치 (DroneBlocks 기본 예제는 인치 사용)

> 참고: 실기에서 `Tello.fly_*` 는 단위 인자를 받지만 **내부적으로는 항상 cm 로 처리**합니다.
> 일관성을 위해 시뮬레이터/실기 모두 `'cm'` 로 통일하는 것을 권장합니다.

---

## 7. 문제 해결

| 증상 | 원인 / 해결 |
|------|------|
| 시뮬레이터가 명령에 반응하지 않음 | Chrome의 Insecure Content 설정 / sim_key 확인 |
| 실기에서 `Did not receive a state packet` | PC가 TELLO-XXXXXX Wi-Fi 에 연결되지 않음 |
| 실기에서 `error` 또는 `out of range` 응답 | 거리값이 20cm 미만이거나 정수가 아님 |
| 드론이 명령 도중 자동 착륙 | 배터리 부족 또는 15초간 무명령 (keepalive 필요) |

추가 이슈는 [DroneBlocks 공식 저장소](https://github.com/dbaldwin/DroneBlocks-Tello-Simulator-With-Python/issues) 에 보고해 주세요.
