import threading
import time
import subprocess
from src.TMC_2209.TMC_2209_StepperDriver import TMC_2209

# May need to swap the - step to achieve proper movement directions
stepR_global = -20000
stepL_global = 20000


def setup_motors():
    global payloadMotor, vertMotor1, vertMotor2
    
    payloadMotor = TMC_2209(5, 6, 26, skip_uart_init=True)
    vertMotor2 = TMC_2209(17, 27, 22, skip_uart_init=True)
    vertMotor1 = TMC_2209(23, 24, 25, skip_uart_init=True)
    
    for motor in [vertMotor1, vertMotor2, payloadMotor]:
        motor.set_acceleration_fullstep(7500)
        motor.set_max_speed_fullstep(7500)
        motor.set_motor_enabled(True)
        motor.set_current_position(0)

def take_snapshot(frame_count=100):
    width = 1920
    height = 1080
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"captured_image_{timestamp}.jpg"        
    command = [
        'fswebcam',
        '-r', f'{width}x{height}',
        '--jpeg', '85',
        '-D', '1', '-F', '80',
        file_name
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Photo taken and saved as '{file_name}'.")
    except subprocess.CalledProcessError:
        print("Failed to capture photo.")

def move_motor_vertically():
    global stepR_global, stepL_global

    threads = [
        threading.Thread(
            target=motor.run_to_position_steps, args=(stepL_global, stepR_global)
        )
        for motor in [vertMotor1, vertMotor2]
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    stepR_global += 25000
    stepL_global -= 25000
    
def testfunc():
    move_motor_vertically()
def move_vrt_home():
    threads = [
        threading.Thread(target=motor.run_to_position_steps, args=(0,))
        for motor in [vertMotor1, vertMotor2]
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def main_motor_movement():
    gantryEndHzn = 40000
    gantryEndVrt = 150000
    stepHzn = -30000
    
    loopcounter = 0
    while abs(vertMotor1.get_current_position()) < gantryEndVrt:
        print(f"Vert Motor: {abs(vertMotor2.get_current_position())} < {gantryEndVrt}")
        print(f"Payload Motor: {payloadMotor.get_current_position()} < {gantryEndHzn}")

        take_snapshot()
        print(payloadMotor.get_current_position())
        time.sleep(.5)
        if loopcounter == 0:
            payloadMotor.run_to_position_steps(-45000)
            take_snapshot()
            loopcounter = 1
        
        payloadMotor.run_to_position_steps(stepHzn)
        take_snapshot()
        stepHzn += 15000
        
        if payloadMotor.get_current_position() >= gantryEndHzn:
            take_snapshot()
            payloadMotor.run_to_position_steps(0)
            print(f"Expected vertical movement.Triggered {payloadMotor.get_current_position()} >= {gantryEndHzn}")
            move_motor_vertically()

            stepHzn = -15000
            loopcounter = 0

    move_vrt_home()

if __name__ == "__main__":
    setup_motors()
    main_motor_movement()
    #move_motor_vertically()
