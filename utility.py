import numpy as np

#define colors in rgb space
BLUE = [0, 0, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
ORANGE = [255, 165, 0]
MAGENTA = [255, 0, 255]
default_colors = np.array([BLUE, RED, GREEN, YELLOW, ORANGE, MAGENTA])
color_names = ['blue', 'red', 'green', 'yellow', 'orange', 'magenta']

def sort_color(rgbValue):
    #classify color based on euclidean distance to default colors
    distances = np.linalg.norm(default_colors - rgbValue, axis=1)
    index = np.argmin(distances)
    return index, color_names[index]

def lane_follower(colorIndex):
    #takes as input an rgb value and returns a steering angle
    #used to follow a lane where left is red and right is blue
    #if color is green, stop
    #classify color
    
    #if color is red, turn right
    if colorIndex == 1:
        return turn_right()
    elif colorIndex == 0:
        return turn_left()
    elif colorIndex == 2:
        return stop()
    else:
        return go_straight()

# functions returning steering rate of left and right wheels
# to be called in state machine (not yet implemented)
# steering rate between 0 and 1, needs to be scaled to actual speed
def stop():
    #stop the car
    return 0,0

def go_straight():
    #go straight
    return 1,1

def turn_right():
    #turn right
    return 1,0

def turn_left():
    #turn left
    return 0,1
    
    