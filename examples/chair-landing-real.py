"""
실제 Tello EDU 기기로 의자 착륙 시퀀스를 수행하는 간단 버전.

사용 전 확인:
  1. PC를 Tello EDU의 Wi-Fi (TELLO-XXXXXX) 에 연결할 것
  2. 드론 주변 안전 공간 확보
  3. 배터리 30% 이상 권장

주의: Tello SDK 의 move 명령은 최소 거리 20cm, 정수만 허용합니다.
      현재 거리값(5, 2.5 등)은 실제 드론에서 거부될 수 있습니다.
      실기 테스트 시 거리를 20 이상 정수로 올려주세요.
"""

from DroneBlocksTelloSimulator.tello import Tello

units = 'cm'

# 1) Tello 객체 생성 (기본 host = 192.168.10.1)
tello = Tello()

# 2) SDK 모드 진입 + state packet 수신 확인
tello.connect()

# 3) 배터리 확인
print(f'배터리: {tello.get_battery()}%')

# 4) 이륙
tello.takeoff()

# 5) 위로 상승
# tello.fly_up(20, units)

# 6) 의자 앞쪽으로 전진
tello.fly_forward(40, units)

# 7) 왼쪽으로 정렬
tello.fly_left(40, units)

# 8) 앞으로 미세 전진
tello.fly_forward(40, units)

# 9) 오른쪽으로 정렬
tello.fly_right(20, units)

# 10) 의자 중심 좌석 위로 후진
tello.fly_backward(20, units)

# 11) 의자 중심 착륙
tello.land()

# 12) 소켓 정리
tello.end()
