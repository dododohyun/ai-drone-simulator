from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager

if __name__ == '__main__':
    sim_key = '3cb6c0ff-854a-413b-8f22-484ba56913d4'
    # sim_key = None

    units = 'cm'

    with DroneBlocksSimulatorContextManager(simulator_key=sim_key) as drone:
        # 이륙
        drone.takeoff()

        # 1) 위로 상승
        #drone.fly_up(10, units)

        # 2) 의자 앞쪽으로 전진
        drone.fly_forward(40, units)

        # 3) 왼쪽으로 정렬
        drone.fly_left(20, units)

        # 4) 앞으로 미세 전진
        drone.fly_forward(20, units)

        # 5) 오른쪽으로 정렬
        drone.fly_right(20, units)

        # 6) 의자 중심 좌석 위로 후진
        drone.fly_backward(10, units)

        # 의자 중심 착륙
        drone.land()
