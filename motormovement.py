import threading
import time
from typing import Dict
# from camera_control import CameraControl
import subprocess
from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209


class MotorControl:
    def __init__(self):
        self.payloadMotor = TMC_2209(5, 6, 26, skip_uart_init=True)
        self.vertMotor2 = TMC_2209(17, 27, 22, skip_uart_init=True)
        self.vertMotor1 = TMC_2209(23, 24, 25, skip_uart_init=True)

        self.width = 1920
        self.height = 1080
        self.gantryEndHzn = 100000
        self.gantryEndVrt = 75000#halfway is about 75000
        self.stepRight = 25000 # this is one
        self.stepLeft = -25000 # this is two
        self.stepHzn = 20000

        self._setup_motors()

    def _setup_motors(self):
        for motor in [self.vertMotor1, self.vertMotor2, self.payloadMotor]:
            motor.set_acceleration_fullstep(2500)
            motor.set_max_speed_fullstep(7000)
            motor.set_motor_enabled(True)
            motor.set_current_position(0)

    def take_snapshot(self, frame_count: int = 100):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"captured_image_{timestamp}.jpg"        
        command = [
            'fswebcam',
            '-r', f'{self.width}x{self.height}',
            '--jpeg', '85',
            '-D', '1', '-F', '80',
            file_name
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Photo taken and saved as '{file_name}'.")
        except subprocess.CalledProcessError:
            print("Failed to capture photo.")

    def main_motor_movement(self):
            while self.vertMotor1.get_current_position() < self.gantryEndVrt:
                print(f"Looping: {self.vertMotor1.get_current_position()} < {self.gantryEndVrt}")
                self.take_snapshot()
                print(self.payloadMotor.get_current_position())
                time.sleep(.5)
                self.move_motor_horizontally()
                self.stepHzn += 20000
                if self.payloadMotor.get_current_position() >= self.gantryEndHzn:
                    self.take_snapshot()
                    self.payloadMotor.run_to_position_steps(0)
                    self.stepHzn = 0

                    self.move_motor_vertically()
                    self.stepRight += 25000
                    self.stepLeft -= 25000
                # if self.payloadMotor.get_current_position() == 0:
                #     self.move_motor_horizontally()
            self.move_vrt_home()


    def move_motor_horizontally(self):
        self.payloadMotor.run_to_position_steps(self.stepHzn)

    def move_motor_vertically(self):
        threads = [
            threading.Thread(
                target=motor.run_to_position_steps, args=(self.stepLeft, self.stepRight)
            )
            for motor in [self.vertMotor1, self.vertMotor2]
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

    # def move_motor_home(self):
    #     for motor in [self.payloadMotor]:
    #         motor.run_to_position_steps(0)


if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.main_motor_movement()
