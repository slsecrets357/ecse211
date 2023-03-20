
#define colors in rgb space
#ground values obtained by taking 20 measurements of each color
BLUE = [150, 255, 230]
RED = [255, 20, 20]
GREEN = [30, 255, 30]
YELLOW = [255, 215, 15]
WHITE = [255,255,255]
ORANGE = [255, 80, 30]
MAGENTA = [255, 200, 200]
default_colors = [BLUE, RED, GREEN, YELLOW, ORANGE, MAGENTA, WHITE]
color_names = ['blue', 'red', 'green', 'yellow', 'orange', 'magenta', 'white']

TRACK_BLUE = [198, 252,  255]
TRACK_RED = [ 255,  38,  17]
TRACK_GREEN = [98, 255,  45]
TRACK_WHITE = [255, 224,  119] #[207, 182,  97]
track_default_colors = [TRACK_BLUE, TRACK_RED, TRACK_GREEN, YELLOW, ORANGE, MAGENTA, TRACK_WHITE]

def euclidean_distance(color_a, color_b):
    """
    Calculate the euclidean distance between two colors.
    """
    r_diff = (color_a[0] - color_b[0]) ** 2
    g_diff = (color_a[1] - color_b[1]) ** 2
    b_diff = (color_a[2] - color_b[2]) ** 2
    return (r_diff + g_diff + b_diff) ** 0.5

def detect_color(rgbValue, track=False):
    if rgbValue[0] is None or rgbValue[1] is None or rgbValue[2] is None:
        print("rgb value is none.")
        return -1, -1
    #normalize rgb values to 0-255
    maxValue = max(rgbValue)
    if maxValue!=0:
        for i in range(3):
            rgbValue[i]*=255/maxValue
    print(rgbValue)
    #classify color based on euclidean distance to default colors
    distances = []
    colors = default_colors if not track else track_default_colors
    for color in colors:
        dist = euclidean_distance(color, rgbValue)
        distances.append(dist)
    minDistance = min(distances)
    index = distances.index(minDistance)
    if minDistance >= 75:
       print("not sure. Ignore this value")
       return -1, -1
    # distances = np.linalg.norm(default_colors - rgbValue, axis=1)
    # index = np.argmin(distances)
    print("Color detected: " + color_names[index] + " error is " + str(minDistance))
    return index, color_names[index]

def lane_follower(colorIndex):
    #takes as input an rgb value and returns a steering angle
    #used to follow a lane where left is red and right is blue
    #if color is green, stop
    #classify color
    
    #if color is red, turn left
    if colorIndex == 1:
        return turn_left()
    elif colorIndex == 0:
        return turn_right()
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
    return 1.2,0
def turn_left():
    #turn left
    return 0,1.2
    
    