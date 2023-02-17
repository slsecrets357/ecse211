from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor
import time
motor = Motor("C")
#motor.reset_encoder()
motor.set_dps(225)
#motor.set_power(0)
#motor.set_limits(100, 360)
print("set position")
print(motor.get_position())
cw = True
t1 = time.time()
while True:
    print("time: ", time.time()-t1)
    t1 = time.time()
    if cw:
        print("clockwise")
        motor.set_position_relative(80)
        cw = not cw
    else:
        print("ccw")
        motor.set_position_relative(-80)
        cw = not cw
    time.sleep(0.5)
print(motor.is_moving())
motor.wait_is_moving()
print("exiting")