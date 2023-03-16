#!/usr/bin/env python3
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor
import time

class Band():
    def __init__(self):
        self.sounds = []
        self.NOSOUND = sound.Sound(duration=0.3, pitch="A4", volume=0)
        self.SOUND1 = sound.Sound(duration=1.57, pitch="A4", volume=75)
        self.SOUND2 = sound.Sound(duration=1.57, pitch="B4", volume=75)
        self.SOUND3 = sound.Sound(duration=1.57, pitch="C5", volume=75)
        self.SOUND4 = sound.Sound(duration=1.57, pitch="D5", volume=75)
        self.sounds.append(self.SOUND1)
        self.sounds.append(self.SOUND2)
        self.sounds.append(self.SOUND3)
        self.sounds.append(self.SOUND4)
        self.touch1 = TouchSensor(1)
        self.touch2 = TouchSensor(2)
        self.touch3 = TouchSensor(3)
        self.motor = Motor("C")
        #self.motor.set_power(100)
        self.wasPressed = [0,0,0]
        self.pressed = [0,0,0]
        self.initialState = True
        self.timer = time.time()
        self.cw = True #determine whether motor is clockwise or ccw
        self.pauseDrum = False
        self.pauseFlute = False
        
    def play(self):
        print("playing")
        self.initialState = True
        while True:
            #check buttons pressed
            self.pressed[0] = self.touch1.is_pressed()
            self.pressed[1] = self.touch2.is_pressed()
            self.pressed[2] = self.touch3.is_pressed()
            
            if not self.initialState:
                if time.time()-self.timer > 0.25:
                    #toggle drum direction every second.
                    self.timer = time.time() #reset timer
                    self.cw = not self.cw #toggle
    #               print("toggle drum direction. clockwise is now ", self.cw)
                if self.pauseDrum:
                    pass
                else:
                    #play drum
                    if self.cw:
                        self.motor.set_position_relative(40)
                    else:
                        self.motor.set_position_relative(-40)
                #motor.set_dps(90)
            for i in range(3):
                #update wasPressed
                if self.pressed[i] and not self.wasPressed[i]:
                    self.wasPressed[i] = 1
                    if self.initialState:
                        print("button pressed, leaving initial state")
                        self.timer = time.time() #reset timer
                        self.initialState = False
            #if a button is released
            if self.wasPressed[0]>self.pressed[0] or self.wasPressed[1]>self.pressed[1] or self.wasPressed[2]>self.pressed[2]:
                #determine state based on wasPressed
                #touch1 is MSB, touch3 is LSB
                self.state = self.wasPressed[0]*4+self.wasPressed[1]*2+self.wasPressed[2]
                print(f"a button is released. performing action {self.state}")
                #perform action based on state
                self.action(self.state)
                #sleep to allow for all buttons to be released
                #print("sleeping..")
                time.sleep(0.01)
                #print("done sleeping")
                #reset wasPressed
                self.wasPressed = [0,0,0]
    def action(self, state):
        if self.state == 1: #pause drum
            if self.pauseDrum:
                print("unpausing drum!!")
                self.motor.set_position(initialPos)
                self.motor.set_limits(dps=80)
                print("drum sleeping.")
                time.sleep(1.5)
                print("drum done sleeping.")
                self.timer = time.time()
                self.cw = True
            else:
                print("pausing drum D:")
                self.motor.set_limits(power=0,dps=0)
                self.motor.set_position(initialPos)
            self.pauseDrum = not self.pauseDrum
        elif self.state == 2: #pause 
            if self.pauseFlute:
                print("Unpausing flute..")
            else:
                print("Pausing flute")
            self.pauseFlute = not self.pauseFlute
        elif self.state == 4:
            print("emergency full stop. reset timer")
            exit()
        elif self.state == 3 or self.state >= 5:
            "Play a single note."
            if self.pauseFlute:
                print("flute is   paused. resume it to play note xd")
                return 
            self.state = 4 if state==3 else state
            print("playing a single note: ", state-3)
            self.sounds[self.state-4].play()#.wait_done()
            #self.sounds[self.state-4].wait_done()
        elif self.state == 0:
            print("no sound")
            NOSOUND.play()
        else: #emergency stop
            print("emergency exit")
            self.motor.set_position(0)
            time.sleep(0.5)
            self.timer = time.time()
            #exit()
        

if __name__=='__main__':
    print("hi world")
    band = Band()
    
    #wait_ready_sensors() # Note: Touch sensors actually have no initialization time
    initialPos = band.motor.get_position()
    print("initial position: ", initialPos)
    band.motor.set_limits(dps=80)
    band.play()

