from motor import Motor
from motor_control import MotorControl

def main():
    motors = {
        'payload': Motor(21, 16, 20, 'payload'),
        'vert1': Motor(17, 27, 22, 'vert1'),
        'vert2': Motor(23, 24, 25, 'vert2')
    }
    
    motor_control = MotorControl(motors)
    motor_control.main_motor_movement()

