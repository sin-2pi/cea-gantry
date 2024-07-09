import time
import cv2
import threading
from typing import Tuple

from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209
from src.TMC_2209._TMC_2209_GPIO_board import Board


class MotorControl:
    def __init__(self):
        self.payloadMotor = TMC_2209(21, 16, 20, skip_uart_init=True)
        self.vertMotor1 = TMC_2209(17, 27, 22, skip_uart_init=True)
        self.vertMotor2 = TMC_2209(23, 24, 25, skip_uart_init=True)

        self.gantryEndHzn = 16000
        self.gantryEndVrt = 5000
        self.stepRight = -1626
        self.stepLeft = 1626
        self.stepHzn = 1600

        self._setup_motors()

    def _setup_motors(self):
        for motor in [self.payloadMotor, self.vertMotor1, self.vertMotor2]:
            motor.set_acceleration_fullstep(2500)
            motor.set_max_speed_fullstep(3000)
            motor.set_motor_enabled(True)
            motor.set_current_position(0)

    def main_motor_movement(self):
        while True:
            self.move_motor_horizontally()
            if self.payloadMotor.get_current_position() > self.gantryEndHzn:
                self.payloadMotor.run_to_position_steps(0)
                self.stepHzn = 1600
                self.move_motor_vertically()
                if self.vertMotor1.get_current_position() > self.gantryEndVrt:
                    self.move_vrt_home()
                    break

    def move_motor_horizontally(self):
        self.camera_snapshot()
        self.payloadMotor.run_to_position_steps(self.stepHzn)
        self.stepHzn += 1600

    def move_motor_vertically(self):
        def move_motor1():
            self.vertMotor1.run_to_position_steps(self.stepLeft)
            self.stepLeft += 1626

        def move_motor2():
            self.vertMotor2.run_to_position_steps(self.stepRight)
            self.stepRight -= 1626

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
            threading.Thread(target=motor.run_to_position_steps, args=(0,))
            for motor in [self.vertMotor1, self.vertMotor2]
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def camera_snapshot(self):
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  # Width
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)  # Height

        frame_count = 0
        target_frame_count = 100

        while True:
            ret, frame = cap.read()

            frame_count += 1
            if frame_count >= target_frame_count:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                file_name = f"captured_image_{timestamp}.jpg"
                cv2.imwrite(file_name, frame)
                break

        cap.release()
        cv2.destroyAllWindows()

    def move_motor_home(self):
        for motor in [self.payloadMotor, self.vertMotor1, self.vertMotor2]:
            motor.run_to_position_steps(0)


if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.main_motor_movement()
