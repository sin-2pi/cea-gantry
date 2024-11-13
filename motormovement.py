import threading
import time
from typing import Dict
# from camera_control import CameraControl
import subprocess
from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209


class MotorControl:
    def __init__(self):
        self.payloadMotor = TMC_2209(21, 16, 20, skip_uart_init=True)
        self.vertMotor2 = TMC_2209(17, 27, 22, skip_uart_init=True)
        self.vertMotor1 = TMC_2209(23, 24, 25, skip_uart_init=True)

        self.width = 1920
        self.height = 1080
        self.gantryEndHzn = 20000
        self.gantryEndVrt = 12000
        self.stepRight = 3000
        self.stepLeft = -3000
        self.stepHzn = 5000

        self._setup_motors()

    def _setup_motors(self):
        for motor in [self.payloadMotor, self.vertMotor1, self.vertMotor2]:
            motor.set_acceleration_fullstep(2500)
            motor.set_max_speed_fullstep(3000)
            motor.set_motor_enabled(True)
            motor.set_current_position(0)

    def take_snapshot(self, frame_count: int = 100):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"captured_image_{timestamp}.jpg"
        
        command = [
            'fswebcam',
            '-r', f'{self.width}x{self.height}',
            '--jpeg', '85',
            '-D', '2', '-F', '100',
            file_name
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Photo taken and saved as '{file_name}'.")
        except subprocess.CalledProcessError:
            print("Failed to capture photo.")

    def main_motor_movement(self):
        while self.payloadMotor.get_current_position() < self.gantryEndHzn:
            self.move_motor_horizontally()
            self.stepHzn += self.stepHzn
            time.sleep(1)
            self.take_snapshot()
            time.sleep(1)
        self.move_motor_vertically()
        self.payloadMotor.run_to_position_steps
        self.stepright -= 3000
        self.stepleft += 3000
        if self.payloadMotor.get_current_position() == 0:
            self.move_motor_horizontally()

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

    def move_motor_home(self):
        for motor in [self.payloadMotor, self.vertMotor1, self.vertMotor2]:
            motor.run_to_position_steps(0)


if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.main_motor_movement()
