import utility
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor, EV3ColorSensor
import time

class StateMachine():
    def __init__(self):
        #states
        self.states = ["initial", "picking up", "lane following", "delivering", "final"]
        self.state = 0
        
        #sensors
        self.laneColorSensor = EV3ColorSensor(1)
        self.cubeColorSensor = EV3ColorSensor(4)
        self.leftWheelMotor = Motor("A")
        self.rightWheelMotor = Motor("D")
        self.leftWheelMotor.set_limits(dps=100, power=50)
        self.rightWheelMotor.set_limits(dps=100, power=50)
        
        #others
        #self.color_names = ['blue', 'red', 'green', 'yellow', 'orange', 'magenta']
        self.color_names = ['blue', 'red', 'green']
        self.cubes = []
        
    def change_state(self, state):
        print("Transitioninig from state " + self.states[self.state] + " to " + self.states[state])
        self.state = state
        
    def run(self):
        while True:
            if self.state == 0: #initial state
                self.change_state(2)
                continue
            elif self.state == 1: #picking up
                pass
            elif self.state == 2: #lane following
                #read sensors
                colorIndex, colorName = utility.sort_color(self.cubeColorSensor.get_rgb())
                if colorIndex == 2: #green detected
                    print("Green detected")
                    self.change_state(3)
                    continue
                leftRatio, rightRatio = utility.lane_follower(colorIndex)
                self.leftWheelMotor.set_power(leftRatio*25)
                self.rightWheelMotor.set_power(rightRatio*25)
                time.sleep(0.5)
                continue
            elif self.state == 3: #delivering
                self.leftWheelMotor.set_power(0)
                self.rightWheelMotor.set_power(0)
                time.sleep(3)
                self.change_state(2)
                continue
            elif self.state == 4: #final
                exit()
                
SM = StateMachine()
SM.run()    
# while True:
#     utility.sort_color(SM.cubeColorSensor.get_rgb())
#     time.sleep(0.5)