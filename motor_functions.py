import time
import cv2

from src.TMC_2209.TMC_2209_StepperDriver import *
from src.TMC_2209._TMC_2209_GPIO_board import Board

# Constructor, sets GPIO pins used to communicate with the RPi5.
payload_motor = TMC_2209(21, 16, 20, skip_uart_init=True)
#vert_motor1 = TMC_2209(17, 27, 22, skip_uart_init=True)
#vert_motor2 = TMC_2209(23, 24, 25, skip_uart_init=True)

# Setting max speed and acceleration in terms of fullsteps per second.
payload_motor.set_acceleration_fullstep(2500)
payload_motor.set_max_speed_fullstep(3000)

# This variable is meant to be the end point for camera data collection, on the horizontal axis.
# Change this
gantry_end_hzn = 16000
gantry_end_vrt = 16000

# This variable is meant to be the distance (in steps) from one vertical tower cell to the next, horizontally.
# Change this
global step




"""
Function that steps the motor to a cells positon in different columns, waits 5 seconds to allow a photo to be taken.
Then continues until the set endpoint of the gantry system is reached and the motor returns to the starting point
"""


def move_motor_horizontally():

    step = 2000
    payload_motor.set_motor_enabled(True)
    payload_motor.set_current_position(0)
    while payload_motor.get_current_position() < gantry_end_hzn:
        payload_motor.run_to_position_steps(step)
        step += 2000
        time.sleep(1)
        camera_snapshot()
        time.sleep(1)
    payload_motor.run_to_position_steps(0)
    #if payload_motor.get_current_position() == 0:
        #move_motor_horizontally()


def move_motor_vertically():
    vert_motor1.run_to_position_steps(1626)
    vert_motor2.run_to_position_steps(1626)


def camera_snapshot():
    cap = cv2.VideoCapture(0)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  # Width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)  # Height

    frame_count = 0
    target_frame_count = 150


    while True:
        ret, frame = cap.read()

        frame_count += 1
        if frame_count >= target_frame_count:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name = f'captured_image_{timestamp}.jpg'
            cv2.imwrite(file_name, frame)
            break

    cap.release()
    cv2.destroyAllWindows()


def move_motor_home():
    pass
