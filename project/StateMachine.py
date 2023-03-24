import utility
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor, EV3ColorSensor
import time

class StateMachine():
    def __init__(self):
        #states
        self.states = ["initial", "cooldown", "lane following", "delivering1: adjust position", "delivering2: rotate platter",
                        "delivering3: dropping cube", "final"]
        self.state = 0
        
        #sensors
        self.laneColorSensor = EV3ColorSensor(3)
        self.cubeColorSensor = EV3ColorSensor(1)
        self.leftWheelMotor = Motor("D")
        self.rightWheelMotor = Motor("A")
        self.leftWheelMotor.set_limits(dps=100, power=50)
        self.rightWheelMotor.set_limits(dps=100, power=50)
        self.rotationMotor = Motor("B")
        self.pushingMotor = Motor("C")
        self.rotationMotor.set_limits(dps=100, power=50)
        self.pushingMotor.set_limits(dps=100, power=50) 
        
        #cubes
        self.cubes = [0,1,2,3,4,5,6] 
        self.cubePointer = 0
        self.cubeDroppedCount = 0

        #others
        self.color_names = ['blue', 'red', 'green', 'yellow', 'orange', 'magenta']
        # self.color_names = ['blue', 'red', 'green']
        self.cubes = []
        self.wheelMotorPower = 18
        self.done = False
        self.deliverColor = None
        self.deliverIndex = None
        self.timer = None
        
    def change_state(self, state):
        print("Transitioninig from state " + self.states[self.state] + " to " + self.states[state])
        self.state = state
        
    def run(self):
        while True:
            if self.state == 0: #initial state
                self.change_state(2)
                continue
            elif self.state == 1: #cooldown
                if self.timer is None:
                    self.timer = time.time()+2
                if time.time()>self.timer:
                    self.timer = None
                    self.change_state(2)
                colorIndex, colorName = utility.detect_color(self.laneColorSensor.get_rgb(), track = True)
                leftRatio, rightRatio = utility.lane_follower(colorIndex)
                self.leftWheelMotor.set_power(leftRatio*self.wheelMotorPower*0.8)
                self.rightWheelMotor.set_power(rightRatio*self.wheelMotorPower*0.8)
                time.sleep(0.35)
                continue
            elif self.state == 2: #lane following
                #read sensors
                colorIndex, colorName = utility.detect_color(self.laneColorSensor.get_rgb(), track = True)
                if colorIndex == 2: #green detected
                    print("Green detected")
                    self.change_state(3)
                    continue
                leftRatio, rightRatio = utility.lane_follower(colorIndex)
                self.leftWheelMotor.set_power(leftRatio*self.wheelMotorPower)
                self.rightWheelMotor.set_power(rightRatio*self.wheelMotorPower)
                time.sleep(0.35)
                continue
            elif self.state == 3: #delivering1: adjusting position
                #TODO: adjust position
                if self.done:
                    self.change_state(4) #go to rotating platter
                    self.done = False
                    continue
                count = 0
                self.leftWheelMotor.set_power(0)
                self.rightWheelMotor.set_power(self.wheelMotorPower)
                while True:
                    colorIndex = -1
                    while colorIndex == -1:
                        colorIndex, colorName = utility.detect_color(self.cubeColorSensor.get_rgb(), track = True)
                    if colorIndex != 6: #white
                        print("color: ", colorName, colorIndex)
                        count+=1
                    if count>=3:
                        break
                    time.sleep(0.08)
                count = 0
                print("rotating out of colored zone...")
                colorIndex, colorName = utility.detect_color(self.cubeColorSensor.get_rgb(), track = True)
                print(f"color is {colorName}")
                while True:
                    colorIndex, colorName = utility.detect_color(self.cubeColorSensor.get_rgb(), track = True)
                    if colorIndex == 6:
                        count+=1
                    if count>=2:
                        print("white detected")
                        break
                    time.sleep(0.08)
                print("hi")
                self.rightWheelMotor.set_position_relative(-65)
                time.sleep(2.2)
                
#                 count=0
#                 while True: 
#                     colorIndex, colorName = utility.detect_color(self.laneColorSensor.get_rgb(), track = True)
#                     if colorIndex != 2:
#                         count+=1
#                     if count >= 2:
#                         break
                self.leftWheelMotor.set_power(0)
                self.rightWheelMotor.set_power(0)
                time.sleep(3)
                # self.change_state(2)
                self.done = True
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
                    #self.deliverIndex = 3
                    while self.deliverColor == -1: #read until color is detected
                        self.deliverColor = utility.detect_color(self.cubeColorSensor.get_rgb(), track = True)[0]
                    print("color to deliver is :", self.deliverColor)
                    self.deliverIndex = self.deliverColor

                    print(f"deliver index is {self.deliverIndex}")
                    if self.deliverIndex >= 6:
                        print("Error: white detected. Attempting to try again...")
                        self.deliverColor = None
                        continue
                    if self.deliverIndex is None:
                        print("Error: color not found. Attempting to try again...")
                        self.deliverColor = None
                        continue
                    print(f"current cube pointer: {self.cubePointer}, deliver index: {self.deliverIndex}")
                    rotation = 60*(self.deliverIndex-self.cubePointer) #calculate rotation in degrees
                    print(f"rotating {rotation} degrees...")
                    self.rotationMotor.set_position_relative(rotation) #rotate platter
                    self.rotationMotor.wait_is_stopped() #wait until rotation is done
                    time.sleep(2)
                    self.cubePointer = self.deliverIndex #update cube pointer
                    self.done = True
                    continue
            elif self.state == 5: #delivering3: dropping cube
                if self.done:
                    newState = 1 if self.cubeDroppedCount < 6 else 6 #go to lane following if not all cubes are dropped, else go to final
                    self.change_state(newState) #go back to lane following
                    self.done = False
                    continue
                print("pushing cube...")
                self.pushingMotor.set_position_relative(-80) #push cube
                self.pushingMotor.wait_is_stopped() #wait until pushing is done
                time.sleep(1)
                print("done pushing cube... reset position")
                self.pushingMotor.set_position_relative(80) #pull cube back
                self.pushingMotor.wait_is_stopped() #wait until pulling is done
                time.sleep(1)
#                 print("moving out of green zone...")
#                 self.leftWheelMotor.set_power(10)
#                 self.rightWheelMotor.set_power(10)
#                 
#                 count = 0
#                 while True: 
#                     colorIndex, colorName = utility.detect_color(self.laneColorSensor.get_rgb(), track = True)
#                     if colorIndex != 2:
#                         count+=1
#                     if count >= 3:
#                         break
 
                self.cubeDroppedCount += 1 #update cube dropped count
                print("cubeDroppedCount: ", self.cubeDroppedCount)
                self.done = True
            elif self.state == 8: #final
                exit()
                
SM = StateMachine()
wait_ready_sensors(True)
SM.run()
# SM.pushingMotor.set_position_relative(-80)
# SM.pushingMotor.wait_is_stopped()
# time.sleep(1)
# print("done waiting")
# SM.pushingMotor.set_position_relative(80)
# time.sleep(1)
# SM.pushingMotor.set_power(0)
# while True:
#     utility.detect_color(SM.cubeColorSensor.get_rgb())
#     time.sleep(0.5)