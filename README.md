# Controlled Environment Agriculture (CEA) Gantry System
![image]({https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue})
![image]({https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white})
![image]({https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white})

### Disclaimer
The motor library used can be found here: `https://github.com/Chr157i4n/TMC2209_Raspberry_Pi`.
Some setup instructions that are used here can also be found in the repository above.

## Environment Setup

1. **Miniconda Installation and Environment Creation**

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

2. **Motor Driver Dependency Installation**

In order to install the required dependencies we will have to run a command:
```
pip install -r requirements.txt
```
Make sure you are in your conda environment when you run this.
