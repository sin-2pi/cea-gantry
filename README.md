# Controlled Environment Agriculture (CEA) Gantry System
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)

The goal of this project is to control a payload on a custom-built gantry system, via Raspberry Pi 5. The payload consists of
- 4K RGB camera module
- RPi5
- TMC2209 motor driver

  
It is intended for data acquisition of plants in a vertical tower hydroponic system. 

**_This project is in progress currently._**

![gantry](https://github.com/user-attachments/assets/ce5efba7-79d5-4fcc-a520-3c04dc56f80d)

## Disclaimer
The motor library used can be found [here](https://github.com/Chr157i4n/TMC2209_Raspberry_Pi).
Some setup instructions that are used here can also be found in the repository that is linked.

# Environment Setup

### **Miniconda Installation and Environment Creation**

- Run the command: 
```bash
node -p "process.arch"
```
- You will install the [miniconda](https://www.anaconda.com/download/success) version with respect to your OS. You may have to restart your terminal in for conda to be active.


- Now to create your environment, you will run the command:
```bash
conda create --name [YOUR ENV NAME]
```

- To activate your environment after it is created, run the command:
```bash
conda activate [YOUR ENV NAME]
```

- You may have to install pip in your environment order to install all the dependencies
```bash
conda install pip
```
### **Motor Driver Dependency Installation**

- In order to install the required dependencies we will have to run a command:
```python
pip install -r requirements.txt
```
*Make sure you are in your conda environment when you run this.*
