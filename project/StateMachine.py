import utility
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor, EV3ColorSensor
import time

class StateMachine():
    def __init__(self):
        #states
        self.states = ["initial", "picking up", "lane following", "delivering1: adjust position", "delivering2: rotate platter",
                        "delivering3: dropping cube", "final"]
        self.state = 0
        
        #sensors
        self.laneColorSensor = EV3ColorSensor(1)
        self.cubeColorSensor = EV3ColorSensor(4)
        self.leftWheelMotor = Motor("A")
        self.rightWheelMotor = Motor("D")
        self.leftWheelMotor.set_limits(dps=100, power=50)
        self.rightWheelMotor.set_limits(dps=100, power=50)
        self.rotationMotor = Motor("B")
        self.pushingMotor = Motor("C")
        self.rotationMotor.set_limits(dps=100, power=50)
        self.pushingMotor.set_limits(dps=100, power=50) 
        
        #cubes
        self.cubes = [0,1,2,3,4,5] 
        self.cubePointer = 0
        self.cubeDroppedCount = 0

        #others
        self.color_names = ['blue', 'red', 'green', 'yellow', 'orange', 'magenta']
        # self.color_names = ['blue', 'red', 'green']
        self.cubes = []
        self.wheelMotorPower = 25
        self.done = False
        
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
                self.leftWheelMotor.set_power(leftRatio*self.wheelMotorPower)
                self.rightWheelMotor.set_power(rightRatio*self.wheelMotorPower)
                time.sleep(0.753)
                continue
            elif self.state == 3: #delivering1: adjusting position
                #TODO: adjust position
                #TODO: drop cube
                if self.done:
                    self.change_state(4) #go to rotating platter
                    self.done = False
                    continue
                self.leftWheelMotor.set_power(0)
                self.rightWheelMotor.set_power(0)
                time.sleep(3)
                self.change_state(2)
                continue
            elif self.state == 4: #delivering2: rotate platter
                if self.done:
                    self.change_state(5) #go to dropping cube
                    self.done = False
                    self.deliverColor = None #reset color
                    self.deliverIndex = None #reset index
                    continue
                if self.deliverColor is None:
                    self.deliverColor = -1
                    while self.deliverColor == -1: #read until color is detected
                        self.deliverColor = utility.sort_color(self.cubeColorSensor.get_rgb())[0]
                    #find index of color
                    for i in range(len(self.cubes)):
                        if self.cubes[i] == self.deliverColor:
                            self.deliverIndex = i
                            break
                    if self.deliverIndex is None:
                        print("Error: color not found. Attempting to try again...")
                        self.deliverColor = None
                        continue
                    rotation = 60*(self.deliverIndex-self.cubePointer) #calculate rotation in degrees
                    self.rotationMotor.set_position_relative(rotation) #rotate platter
                    self.rotationMotor.wait_is_stopped() #wait until rotation is done
                    self.cubePointer = self.deliverIndex #update cube pointer
                    self.done = True
                    continue
            elif self.state == 5: #delivering3: dropping cube
                if self.done:
                    newState = 2 if self.cubeDroppedCount < 6 else 6 #go to lane following if not all cubes are dropped, else go to final
                    self.change_state(newState) #go back to lane following
                    self.done = False
                    continue
                self.pushingMotor.set_position_relative(60) #push cube
                self.pushingMotor.wait_is_stopped() #wait until pushing is done
                self.leftWheelMotor.set_position_relative(360) #move forward 1 tile to exit green zone
                self.rightWheelMotor.set_position_relative(360) #move forward 1 tile
                self.leftWheelMotor.wait_is_stopped() #wait until moving is done
                self.rightWheelMotor.wait_is_stopped() 
                self.cubeDroppedCount += 1 #update cube dropped count
                self.done = True
            elif self.state == 6: #final
                exit()
                
SM = StateMachine()
SM.run()    
# while True:
#     utility.sort_color(SM.cubeColorSensor.get_rgb())
#     time.sleep(0.5)