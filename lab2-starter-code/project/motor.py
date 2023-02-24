from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, Motor
import time
motor = Motor("C")
#motor.reset_encoder()
motor.reset_encoder()
# print("pos1: ", motor.get_position())
# motor.set_position(90)
# print("pos2: ", motor.get_position())
# motor.set_limits(power=30, dps=180)
# print("pos3: ", motor.get_position())
# time.sleep(3)
# print("done sleepin")
# print("pos4: ", motor.get_position())
# #motor.set_position(-50)
# print("pos5: ", motor.get_position())
motor.set_position(0)
#motor.set_power(0)
#motor.set_limits(100, 360)
# print("set position")
# print(motor.get_position())
# cw = True
# t1 = time.time() # Get time in sec
# while True:
# #     print("time: ", time.time()-t1)
#     if time.time()>t1+0.5:
#         t1 = time.time()
#         cw = not cw
#     if cw:
# #         print("clockwise")
#         motor.set_position_relative(-40)
#         #cw = not cw
#     else:
# #         print("ccw")
#         motor.set_position_relative(40)
        #cw = not cw
# print(motor.is_moving())
# #motor.wait_is_moving()
# print("exiting")