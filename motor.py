from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209

class Motor:
    def __init__(self, enable_pin: int, step_pin: int, dir_pin: int, name: str):
        self.name = name
        self.motor = TMC_2209(enable_pin, step_pin, dir_pin, skip_uart_init=True)
        self._setup_motor()

    def _setup_motor(self):
        self.motor.set_acceleration_fullstep(2500)
        self.motor.set_max_speed_fullstep(3000)
        self.motor.set_motor_enabled(True)
        self.motor.set_current_position(0)

    def move_to_position(self, steps: int):
        self.motor.run_to_position_steps(steps)

    def get_current_position(self) -> int:
        return self.motor.get_current_position()