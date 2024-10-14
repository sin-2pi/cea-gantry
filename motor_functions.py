import time
import cv2
import threading
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209


class Motor(ABC):
    def __init__(self, name: str, pin_step: int, pin_dir: int, pin_en: int):
        self.name = name
        self.motor = TMC_2209(pin_step, pin_dir, pin_en, skip_uart_init=True)
        self._setup_motor()

    def _setup_motor(self):
        self.motor.set_acceleration_fullstep(2500)
        self.motor.set_max_speed_fullstep(3000)
        self.motor.set_motor_enabled(True)
        self.motor.set_current_position(0)

    @abstractmethod
    def move(self, steps: int):
        pass

    def move_to_home(self):
        self.motor.run_to_position_steps(0)

    def get_position(self) -> int:
        return self.motor.get_current_position()


class HorizontalMotor(Motor):
    def __init__(
        self, name: str, pin_step: int, pin_dir: int, pin_en: int, step_size: int
    ):
        super().__init__(name, pin_step, pin_dir, pin_en)
        self.step_size = step_size

    def move(self, steps: int):
        self.motor.run_to_position_steps(steps * self.step_size)


class VerticalMotor(Motor):
    def __init__(
        self, name: str, pin_step: int, pin_dir: int, pin_en: int, step_size: int
    ):
        super().__init__(name, pin_step, pin_dir, pin_en)
        self.step_size = step_size

    def move(self, steps: int):
        self.motor.run_to_position_steps(steps * self.step_size)


class MotorFactory:
    @staticmethod
    def create_motor(motor_config: Dict) -> Motor:
        motor_type = motor_config["type"]
        if motor_type == "horizontal":
            return HorizontalMotor(
                motor_config["name"],
                motor_config["pin_step"],
                motor_config["pin_dir"],
                motor_config["pin_en"],
                motor_config["step_size"],
            )
        elif motor_type == "vertical":
            return VerticalMotor(
                motor_config["name"],
                motor_config["pin_step"],
                motor_config["pin_dir"],
                motor_config["pin_en"],
                motor_config["step_size"],
            )
        else:
            raise ValueError(f"Unknown motor type: {motor_type}")


class Camera:
    def __init__(self, camera_id: int = 0, width: int = 3840, height: int = 2160):
        self.camera_id = camera_id
        self.width = width
        self.height = height

    def take_snapshot(self, frame_count: int = 100):
        cap = cv2.VideoCapture(self.camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        for _ in range(frame_count):
            ret, frame = cap.read()

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"captured_image_{timestamp}.jpg"
        cv2.imwrite(file_name, frame)

        cap.release()
        cv2.destroyAllWindows()


class GantrySystem:
    def __init__(self, motor_configs: List[Dict], camera: Camera):
        self.motors = {
            config["name"]: MotorFactory.create_motor(config)
            for config in motor_configs
        }
        self.camera = camera
        self.gantry_end_hzn = 16000
        self.gantry_end_vrt = 5000

    def move_horizontally(self, steps: int):
        self.camera.take_snapshot()
        self.motors["payload"].move(steps)

    def move_vertically(self, steps: int):
        threads = [
            threading.Thread(target=self.motors["vertical1"].move, args=(steps,)),
            threading.Thread(target=self.motors["vertical2"].move, args=(-steps,)),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def move_all_to_home(self):
        for motor in self.motors.values():
            motor.move_to_home()

    def main_movement(self):
        horizontal_steps = 0
        vertical_steps = 0

        while True:
            self.move_horizontally(1)
            horizontal_steps += 1

            if (
                horizontal_steps * self.motors["payload"].step_size
                > self.gantry_end_hzn
            ):
                self.motors["payload"].move_to_home()
                horizontal_steps = 0
                self.move_vertically(1)
                vertical_steps += 1

                if (
                    vertical_steps * self.motors["vertical1"].step_size
                    > self.gantry_end_vrt
                ):
                    self.move_all_to_home()
                    break


if __name__ == "__main__":
    motor_configs = [
        {
            "name": "payload",
            "type": "horizontal",
            "pin_step": 21,
            "pin_dir": 16,
            "pin_en": 20,
            "step_size": 1600,
        },
        {
            "name": "vertical1",
            "type": "vertical",
            "pin_step": 17,
            "pin_dir": 27,
            "pin_en": 22,
            "step_size": 1626,
        },
        {
            "name": "vertical2",
            "type": "vertical",
            "pin_step": 23,
            "pin_dir": 24,
            "pin_en": 25,
            "step_size": 1626,
        },
    ]
    camera = Camera()
    gantry_system = GantrySystem(motor_configs, camera)
    gantry_system.main_movement()
