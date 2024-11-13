# Gantry System Hardware Readme

## Motor Wiring Diagram and Information

### TMC2209 Carrier Board $\rightarrow$ Motor Connection Diagram
<img src="https://github.com/user-attachments/assets/49e3a8bd-048e-41e9-b77b-b238d9b5d681" width="650"/>

This is a relevant diagram for 6 pin stepper motor connecting cables, on the motor side. $1A (Green)$ and $1B (Black)$ must always be on the same side, as show in the diagram. $2A (Blue)$ and $2B (Red)$ must always be on the same side as well. The order does not matter, it is only important that the grouped wires are connected on the same side, in the fashion shown.

### TMC2209 Carrier Board $\rightarrow$ RPi5 Wiring Guide
<img src="https://github.com/user-attachments/assets/f501f416-310e-4cc3-bd5a-4eb8b1e688c3" width="650"/>

**EN, STEP, DIR**
- EN: Connect to any open GPIO pin on the RPi5, one that you have selected as the $EN$ pin in $motor_functions.py$.
- STEP: Connect to any open GPIO pin on the RPi5, one that you have selected as the $STEP$ pin in $motor_functions.py$.
- DIR: Connect to any open GPIO pin on the RPi5, one that you have selected as the $DIR$ pin in $motor_functions.py$.

**GROUND**

Connect the ground to a corresponding ground GPIO pin on the RPi5.

**3.3V POWER**

Connect the 3.3v power a corresponding 3.3v power GPIO  pin on the RPi5.

NOTE: *3.3v power and ground can be daisy chained from multiple (tested up to 3) carrier boards. This is for space efficiency, if the wires are daisy chained between carrier boards, you will only have to take ONE 3.3v power pin and ONE ground pin* 
