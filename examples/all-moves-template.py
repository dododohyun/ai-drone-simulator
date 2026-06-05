"""
========================================================================
 Tello Simulator - 모든 동작 종합 템플릿 (기출문제용)
========================================================================
 목적:
   - 어떤 경로 문제가 나와도 응용 가능하도록 "모든 이동 명령"을 포함
   - MISSION 리스트만 수정하면 새 경로로 즉시 시뮬레이션 가능
   - 정확도와 속도를 동시에 잡기 위해 set_speed + 좌표이동(fly_to_xyz) 활용

 사용법:
   1) sim_key 본인 키로 교체
   2) UNITS, SPEED 설정
   3) MISSION 리스트에 동작 튜플을 순서대로 추가
   4) python all-moves-template.py 실행

 지원하는 동작 (명령어 형식):
   ("takeoff",)
   ("land",)
   ("up",     dist)              # 상승
   ("down",   dist)              # 하강
   ("fwd",    dist)              # 직진
   ("back",   dist)              # 후진
   ("left",   dist)              # 좌이동
   ("right",  dist)              # 우이동
   ("xyz",    x, y, z)           # 대각선/3D 한번에 (정확도+속도 최고)
   ("curve",  x1, y1, z1, x2, y2, z2)   # 곡선 경로
   ("yaw_l",  deg)               # 좌회전
   ("yaw_r",  deg)               # 우회전
   ("flip_l",) ("flip_r",) ("flip_f",) ("flip_b",)   # 플립
   ("speed",  cm_per_s)          # 속도 변경
   ("wait",   sec)               # 대기 (필요시)
========================================================================
"""

import time
from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager


# ===== 설정 ==============================================================
SIM_KEY = '3cb6c0ff-854a-413b-8f22-484ba56913d4'   # 본인 시뮬레이터 키
UNITS   = 'cm'                                      # 'cm' 또는 'in'
SPEED   = 80                                        # cm/s (10 ~ 100)


# ===== 미션 경로 (여기만 수정하면 됨) =====================================
# 아래 예시는 "모든 가능성"을 보여주는 데모 경로.
# 새 문제를 풀때는 이 리스트만 다시 작성하면 됨.
MISSION = [
    ("takeoff",),

    # --- 1) 기본 6방향 직선 이동 (상승/하강/직진/후진/좌/우) ---
    ("up",    50),
    ("fwd",   60),
    ("right", 40),
    ("back",  30),
    ("left",  40),
    ("down",  20),

    # --- 2) 대각선/3D 이동 (정확도+속도 최고: 한번에 도착) ---
    # 현재 위치에서 (x=+50 앞, y=+50 좌, z=+30 위) 만큼 이동
    ("xyz",   50, 50, 30),
    ("xyz",  -50, -50, -30),    # 반대 대각선으로 복귀

    # --- 3) 회전 (yaw) ---
    ("yaw_r", 90),    # 우회전 90도
    ("fwd",   40),    # 회전 후 직진
    ("yaw_l", 90),    # 좌회전 90도 (원상 복귀)

    # --- 4) 곡선 경로 (두 점을 지나는 호) ---
    # (x1,y1,z1) 경유점, (x2,y2,z2) 도착점
    ("curve", 50, 50, 0,  100, 0, 0),

    # --- 5) 플립 (공중제비) ---
    ("flip_f",),
    # ("flip_b",), ("flip_l",), ("flip_r",)   # 필요시 주석 해제

    # --- 6) 속도를 바꿔서 다시 이동 (속도 비교용) ---
    ("speed", 50),
    ("fwd",   30),
    ("speed", 100),
    ("back",  30),

    ("speed", 10),
    ("fwd",   100),
    ("speed", 200),
    ("back",  100),
    
    ("land",),
]


# ===== 실행기 (수정 불필요) ===============================================
def run(drone, mission):
    """MISSION 리스트를 순서대로 실행."""
    handlers = {
        "takeoff": lambda a: drone.takeoff(),
        "land":    lambda a: drone.land(),
        "up":      lambda a: drone.fly_up(a[0], UNITS),
        "down":    lambda a: drone.fly_down(a[0], UNITS),
        "fwd":     lambda a: drone.fly_forward(a[0], UNITS),
        "back":    lambda a: drone.fly_backward(a[0], UNITS),
        "left":    lambda a: drone.fly_left(a[0], UNITS),
        "right":   lambda a: drone.fly_right(a[0], UNITS),
        "xyz":     lambda a: drone.fly_to_xyz(a[0], a[1], a[2], UNITS),
        "curve":   lambda a: drone.fly_curve(a[0], a[1], a[2], a[3], a[4], a[5], UNITS),
        "yaw_l":   lambda a: drone.yaw_left(a[0]),
        "yaw_r":   lambda a: drone.yaw_right(a[0]),
        "flip_l":  lambda a: drone.flip_left(),
        "flip_r":  lambda a: drone.flip_right(),
        "flip_f":  lambda a: drone.flip_forward(),
        "flip_b":  lambda a: drone.flip_backward(),
        "speed":   lambda a: drone.set_speed(a[0]),
        "wait":    lambda a: time.sleep(a[0]),
    }

    for i, step in enumerate(mission, 1):
        cmd, args = step[0], step[1:]
        if cmd not in handlers:
            print(f"[{i}] 알 수 없는 명령: {cmd}  → 건너뜀")
            continue
        print(f"[{i}] {cmd} {args}")
        handlers[cmd](args)


if __name__ == '__main__':
    with DroneBlocksSimulatorContextManager(simulator_key=SIM_KEY) as drone:
        drone.set_speed(SPEED)   # 시작 속도 고정 → 정확도/속도 일관성
        run(drone, MISSION)
