import inquirer
from yaspin import yaspin
# import motormovement

spinner = yaspin()
asciiart = r"""
 _   _       _                    _ _                  __   _    _                       _                
| | | |     (_)                  (_) |                / _| | |  | |                     (_)               
| | | |_ __  ___   _____ _ __ ___ _| |_ _   _    ___ | |_  | |  | |_   _  ___  _ __ ___  _ _ __   __ _    
| | | | '_ \| \ \ / / _ \ '__/ __| | __| | | |  / _ \|  _| | |/\| | | | |/ _ \| '_ ` _ \| | '_ \ / _` |   
| |_| | | | | |\ V /  __/ |  \__ \ | |_| |_| | | (_) | |   \  /\  / |_| | (_) | | | | | | | | | | (_| |   
 \___/|_| |_|_| \_/ \___|_|  |___/_|\__|\__, |  \___/|_|    \/  \/ \__, |\___/|_| |_| |_|_|_| |_|\__, |   
                                         __/ |                      __/ |                         __/ |   
                                        |___/                      |___/                         |___/    
______ _             _     _____      _                                                                   
| ___ \ |           | |   /  ___|    (_)                                                                  
| |_/ / | __ _ _ __ | |_  \ `--.  ___ _  ___ _ __   ___ ___                                               
|  __/| |/ _` | '_ \| __|  `--. \/ __| |/ _ \ '_ \ / __/ _ \                                              
| |   | | (_| | | | | |_  /\__/ / (__| |  __/ | | | (_|  __/                                              
\_|   |_|\__,_|_| |_|\__| \____/ \___|_|\___|_| |_|\___\___|                                                                                                                              
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    


"""
print(asciiart)


questions = [
    inquirer.List('functionality',
                  message="Choose a functionality",
                  choices=['Data Collection', 'Image Export'])
]
answer = inquirer.prompt(questions)

if answer.get("functionality") == "Data Collection":
    print("Collecting data...")
    # motormovement.main_motor_movement()
if answer.get("functionality") == "Image Export":
    print("Export images...")
