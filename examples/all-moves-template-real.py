"""
========================================================================
 실제 Tello EDU - 모든 동작 종합 템플릿 (기출문제용)
========================================================================
 목적:
   - all-moves-template.py (시뮬레이터용) 의 실기기 버전
   - MISSION 리스트만 수정하면 새 경로로 즉시 실기 비행 가능

 사용 전 확인:
   1) PC 를 Tello EDU 의 Wi-Fi (TELLO-XXXXXX) 에 연결
   2) 드론 주변 충분한 안전 공간 확보 (특히 플립/곡선 동작 시)
   3) 배터리 30% 이상 권장
   4) 천장/장애물/사람 없는 곳에서 실행

 실기기 제약사항 (시뮬레이터와 다른 점):
   - 이동 거리: 20 ~ 500 cm, 정수만 허용 (20 미만은 거부됨)
   - 속도(set_speed): 10 ~ 100 cm/s
   - fly_to_xyz: 각 좌표 -500 ~ 500, 단 -20 ~ 20 사이 값은 사용 불가
   - flip 은 배터리 50% 이상에서만 동작
   - 명령 사이 자동 대기 없음 → 필요시 ("wait", sec) 사용

 지원 동작:
   ("takeoff",) / ("land",)
   ("up"|"down"|"fwd"|"back"|"left"|"right", dist)
   ("xyz",   x, y, z)
   ("curve", x1, y1, z1, x2, y2, z2)
   ("yaw_l"|"yaw_r", deg)
   ("flip_l",) ("flip_r",) ("flip_f",) ("flip_b",)
   ("speed", cm_per_s)
   ("wait",  sec)
========================================================================
"""

import time
from DroneBlocksTelloSimulator.tello import Tello


# ===== 설정 ==============================================================
UNITS = 'cm'        # 'cm' 또는 'in'
SPEED = 30          # 초기 속도 (실기기는 30~50 권장, 최대 100)


# ===== 미션 경로 (여기만 수정하면 됨) =====================================
# 주의: 실기기는 최소 이동거리 20cm. 20 미만 값은 드론이 거부함.
MISSION = [
    ("takeoff",),

    # --- 1) 기본 6방향 직선 이동 ---
    ("up",    50),
    ("fwd",   60),
    ("right", 40),
    ("back",  30),
    ("left",  40),
    ("down",  20),

    # --- 2) 대각선/3D 이동 ---
    ("xyz",   50, 50, 30),
    ("xyz",  -50, -50, -30),

    # --- 3) 회전 (yaw) ---
    ("yaw_r", 90),
    ("fwd",   40),
    ("yaw_l", 90),

    # --- 4) 곡선 경로 ---
    ("curve", 50, 50, 0,  100, 0, 0),

    # --- 5) 플립 (배터리 50% 이상 필요) ---
    ("flip_f",),

    # --- 6) 속도 변경 ---
    ("speed", 50),
    ("fwd",   30),
    ("speed", 100),
    ("back",  30),

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
    tello = Tello()
    tello.connect()
    print(f'배터리: {tello.get_battery()}%')

    try:
        tello.set_speed(SPEED)
        run(tello, MISSION)
    finally:
        tello.end()
