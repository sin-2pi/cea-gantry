# Controlled Environment Agriculture (CEA) Gantry System

### Disclaimer
The motor library used can be found here: `https://github.com/Chr157i4n/TMC2209_Raspberry_Pi`.
Some setup instructions that are used here can also be found in the repository above.

## Environment Setup

**Miniconda Installation and Environment Creation**

Run the command: 
```
node -p "process.arch"
```
You will install the miniconda version with respect to your OS. You may have to restart your terminal in for conda to be active.

Now to create your environment, you will run the command:
```
conda create --name tmc2209
```

To activate your environment after it is created, run the command:
```
conda activate tmc2209
```

**Motor Driver Dependency Installation**

In order to install the required dependencies we will have to run a few commands:
```
pip3 install TMC-2209-Raspberry-Pi
```
and
```
pip3 install gpiozero
```
