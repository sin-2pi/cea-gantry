import time
import cv2
import threading

from src.TMC_2209.TMC_2209_StepperDriver import *
from src.TMC_2209._TMC_2209_GPIO_board import Board

# Constructor, sets GPIO pins used to communicate with the RPi5.
payloadMotor = TMC_2209(21, 16, 20, skip_uart_init=True)
vertMotor1 = TMC_2209(17, 27, 22, skip_uart_init=True)
vertMotor2 = TMC_2209(23, 24, 25, skip_uart_init=True)

# Setting max speed and acceleration in terms of fullsteps per second.
payloadMotor.set_acceleration_fullstep(2500)
payloadMotor.set_max_speed_fullstep(3000)

# This variable is meant to be the end point for camera data collection, on the horizontal axis.
# Change this
gantryEndHzn = 16000
gantryEndVrt = 16000

# This variable is meant to be the distance (in steps) from one vertical tower cell to the next, horizontally.
# Change this
global step




"""
Function that steps the motor to a cells positon in different columns, waits 5 seconds to allow a photo to be taken.
Then continues until the set endpoint of the gantry system is reached and the motor returns to the starting point
"""


def mainMotorMovement():

    step = 1626
    payloadMotor.set_motor_enabled(True)
    vertMotor1.set_motor_enabled(True)
    vertMotor2.set_motor_enabled(True)

    payloadMotor.set_current_position(0)
    vertMotor1.set_current_position(0)
    vertMotor2.set_current_position(0)

    while vertMotor1.get_current_position() < gantryEndVrt:
        moveMotorVertically()
        step += 1626
        time.sleep(1)
        cameraSnapshot()
        time.sleep(1)
    moveVrtHome()
    if payloadMotor.get_current_position() == 0:
        moveMotorHorizontally()


def moveMotorHorizontally():
    payloadMotor.run_to_position_steps()

def moveMotorVertically():
    def verticalMovement1(step):
        vertMotor1.run_to_position_steps(step)

    def verticalMovement2(step):
        vertMotor2.run_to_position_steps(step)

    thread1 = threading.Thread(target=verticalMovement1)
    thread2 = threading.Thread(target=verticalMovement2)

    thread1.start()
    thread2.start()


    thread1.join()
    thread2.join()

def moveVrtHome():
    def verticalHome1():
        vertMotor1.run_to_position_steps(0)

    def verticalHome2():
        vertMotor2.run_to_position_steps(0)

    thread3 = threading.Thread(target=verticalHome1)
    thread4 = threading.Thread(target=verticalHome2)

    thread3.start()
    thread4.start()


    thread3.join()
    thread4.join()

def cameraSnapshot():
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

