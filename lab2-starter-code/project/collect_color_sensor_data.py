#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from time import sleep

COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR= EV3ColorSensor(1)
TOUCH_SENSOR = TouchSensor(3)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

def detect_color():
    f = open(COLOR_SENSOR_DATA_FILE, 'a')
    rgb = COLOR_SENSOR.get_rgb()
    print(COLOR_SENSOR.get_rgb())
    f.write(str(rgb) + "\n")
    f.close()
    return rgb
    
    
    
def collect_color_sensor_data():
    "Collect color sensor data."
    f = open(COLOR_SENSOR_DATA_FILE, 'w')
    try:
        wasPressed = False
        while True:
            #play_sound()
            if(TOUCH_SENSOR.is_pressed() and (not wasPressed)):
                detect_color()
                wasPressed = True
            elif ((not TOUCH_SENSOR.is_pressed()) and wasPressed):
                wasPressed = False
            sleep(0.2)  
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print("exception occured")
    finally:
        print("Done testing Colors")
        #f.close()
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    collect_color_sensor_data()
