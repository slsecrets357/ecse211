#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

SOUND = sound.Sound(duration=0.3, pitch="A5", volume=100)
TOUCH_SENSOR = TouchSensor(3)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            #play_sound()
            if(TOUCH_SENSOR.is_pressed()):
                print("button pressed")
                play_sound()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print("exception occured")
        exit()


if __name__=='__main__':
    print("running")
    #play_sound()
    # TODO Implement this function
    play_sound_on_button_press()
    
    
