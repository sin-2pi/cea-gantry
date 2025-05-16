import threading
import time
import subprocess
from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209

# OOP solution, needs to be tested but should work

class MotorController:
    """
    Class to manage a single motor and its operations.
    """
    def __init__(self, step_pin, dir_pin, enable_pin, skip_uart_init=True):
        self.motor = TMC_2209(step_pin, dir_pin, enable_pin, skip_uart_init=skip_uart_init)
        self.configure_motor()
        
    def configure_motor(self):
        """Configure the motor with default settings."""
        self.motor.set_acceleration_fullstep(7500)
        self.motor.set_max_speed_fullstep(7500)
        self.motor.set_motor_enabled(True)
        self.motor.set_current_position(0)
    
    def run_to_position_steps(self, position):
        """Run the motor to a specific position."""
        self.motor.run_to_position_steps(position)
    
    def get_current_position(self):
        """Get the current position of the motor."""
        return self.motor.get_current_position()


class CameraController:
    """
    Class to manage camera operations.
    """
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
    
    def take_snapshot(self):
        """Take a snapshot using the camera."""
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


class GantrySystem:
    """
    Main class to manage the gantry system including motors and camera.
    """
    def __init__(self):
        # Initialize motor controllers
        self.payload_motor = MotorController(5, 6, 26)
        self.vert_motor1 = MotorController(23, 24, 25)
        self.vert_motor2 = MotorController(17, 27, 22)
        
        # Initialize camera controller
        self.camera = CameraController()
        
        # Initialize step values
        self.step_r = 25000
        self.step_l = -25000
        
        # Movement limits
        self.gantry_end_hzn = 40000
        self.gantry_end_vrt = 150000
    
    def move_motor_vertically(self):
        """Move vertical motors using threads."""
        threads = []
        
        # Create thread for vert_motor1
        thread1 = threading.Thread(
            target=self.vert_motor1.run_to_position_steps,
            args=(self.step_l,)
        )
        threads.append(thread1)
        
        # Create thread for vert_motor2
        thread2 = threading.Thread(
            target=self.vert_motor2.run_to_position_steps,
            args=(self.step_r,)
        )
        threads.append(thread2)
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            
        # Update step values for next vertical movement
        self.step_r += 25000
        self.step_l -= 25000
    
    def move_vrt_home(self):
        """Move vertical motors back to home position."""
        threads = []
        
        # Create thread for vert_motor1
        thread1 = threading.Thread(
            target=self.vert_motor1.run_to_position_steps,
            args=(0,)
        )
        threads.append(thread1)
        
        # Create thread for vert_motor2
        thread2 = threading.Thread(
            target=self.vert_motor2.run_to_position_steps,
            args=(0,)
        )
        threads.append(thread2)
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    
    def main_motor_movement(self):
        """Main motor movement sequence."""
        step_hzn = -15000
        loop_counter = 0
        
        while abs(self.vert_motor1.get_current_position()) < self.gantry_end_vrt:
            print(f"Vert Motor: {abs(self.vert_motor2.get_current_position())} < {self.gantry_end_vrt}")
            print(f"Payload Motor: {self.payload_motor.get_current_position()} < {self.gantry_end_hzn}")

            # First movement is to position -45000 (changed from -30000)
            if loop_counter == 0:
                self.payload_motor.run_to_position_steps(-45000)
                self.camera.take_snapshot()
                loop_counter = 1
            
            self.payload_motor.run_to_position_steps(step_hzn)
            self.camera.take_snapshot()
            step_hzn += 15000
            
            if self.payload_motor.get_current_position() >= self.gantry_end_hzn:
                self.camera.take_snapshot()
                self.payload_motor.run_to_position_steps(0)
                print(f"Expected vertical movement. Triggered {self.payload_motor.get_current_position()} >= {self.gantry_end_hzn}")
                self.move_motor_vertically()

                step_hzn = -15000
                loop_counter = 0

        self.move_vrt_home()


def main():
    """Main function to run the gantry system."""
    gantry = GantrySystem()
    gantry.main_motor_movement()


if __name__ == "__main__":
    main()
