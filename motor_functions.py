import threading
from typing import Dict
from motor import Motor

class MotorControl:
    def __init__(self, motors: Dict[str, Motor]):
        self.motors = motors
        self.gantry_end_hzn = 16000
        self.gantry_end_vrt = 5000
        self.step_right = -1626
        self.step_left = 1626
        self.step_hzn = 1600

    def main_motor_movement(self):
        while True:
            self.move_motor_horizontally()
            if self.motors['payload'].get_current_position() > self.gantry_end_hzn:
                self.motors['payload'].move_to_position(0)
                self.step_hzn = 1600
                self.move_motor_vertically()
                if self.motors['vert1'].get_current_position() > self.gantry_end_vrt:
                    self.move_vrt_home()
                    break

    def move_motor_horizontally(self):
        CameraControl.take_snapshot()
        self.motors['payload'].move_to_position(self.step_hzn)
        self.step_hzn += 1600

    def move_motor_vertically(self):
        def move_motor1():
            self.motors['vert1'].move_to_position(self.step_left)
            self.step_left += 1626

        def move_motor2():
            self.motors['vert2'].move_to_position(self.step_right)
            self.step_right -= 1626

        threads = [
            threading.Thread(target=move_motor1),
            threading.Thread(target=move_motor2),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def move_vrt_home(self):
        threads = [
            threading.Thread(target=self.motors[motor].move_to_position, args=(0,))
            for motor in ['vert1', 'vert2']
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def move_all_motors_home(self):
        for motor in self.motors.values():
            motor.move_to_position(0)
