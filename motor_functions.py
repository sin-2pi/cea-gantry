import time
from src.TMC_2209.TMC_2209_StepperDriver import *
from src.TMC_2209._TMC_2209_GPIO_board import Board

# Constructor, sets GPIO pins used to communicate with the RPi5.
tmc = TMC_2209(21, 16, 20, skip_uart_init=True)

# Setting max speed and acceleration in terms of fullsteps per second.
tmc.set_acceleration_fullstep(1000)
tmc.set_max_speed_fullstep(3000)

# This variable is meant to be the end point for camera data collection, on the horizontal axis.
# Change this
gantry_end = 30000

# This variable is meant to be the distance (in steps) from one vertical tower cell to the next, horizontally.
# Change this
step = 200


"""
Function that steps the motor to a cells positon in different columns, waits 5 seconds to allow a photo to be taken.
Then continues until the set endpoint of the gantry system is reached and the motor returns to the starting point
"""


def move_motor_horizontally():
    tmc.set_motor_enabled(True)
    while tmc.get_current_position() < gantry_end:
        tmc.run_to_position_steps(step)
        time.sleep(5)
    tmc.run_to_position_steps(0)


def move_motor_vertically():
    pass


def camera_snapshot():
    pass


def move_motor_home():
    pass
