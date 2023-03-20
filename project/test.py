import utility
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor, EV3ColorSensor
import time

def run(self):
    while True:
        if self.state == 2: #lane following
            #check for transition events
            colorIndex, colorName = utility.detect_color(self.cubeColorSensor.get_rgb(), track = True)
            if colorIndex == 2: #green detected
                print("Green detected")
                self.change_state(3)
                continue
            #publish wheel steering rates
            leftRatio, rightRatio = utility.lane_follower(colorIndex)
            self.leftWheelMotor.set_power(leftRatio*self.wheelMotorPower)
            self.rightWheelMotor.set_power(rightRatio*self.wheelMotorPower)
            time.sleep(0.753)
            continue
        elif self.state == 3: #delivering1: adjusting position
            #check for transition events
            #do what the state is supposed to do