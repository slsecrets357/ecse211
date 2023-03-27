import numpy as np

Yellow = np.array([

[199, 197, 15],
[209, 207, 18],
[207, 205, 17],
[202, 203, 16],
[271, 257, 19],
[260, 248, 18],
[301, 236, 19],
[286, 257, 18],
[288, 264, 19],
[296, 269, 19],
[299, 255, 21],
[309, 258, 22],
[274, 256, 18],
[282, 257, 18],
[251, 245, 18],
[251, 243, 17],
[283, 260, 19],
[304, 265, 20],
[298, 248, 20],
[307, 255, 20]
])

Purple = np.array([

[204, 40, 29],
[199, 39, 28],
[220, 37, 28],
[220, 34, 27],
[216, 32, 28],
[199, 26, 22],
[212, 29, 24],
[218, 33, 26],
[215, 33, 29],
[219, 33, 26],
[148, 20, 16],
[202, 27, 24],
[214, 32, 27],
[212, 28, 25],
[201, 32, 26],
[197, 27, 24],
[154, 20, 17],
[179, 24, 21],
[213, 33, 26],
[213, 35, 25],
[217, 32, 25]
])
Orange = np.array([

[222, 80, 13],
[213, 79, 14],
[208, 78, 13],
[210, 79, 11],
[279, 94, 14],
[243, 89, 11],
[229, 85, 11],
[284, 99, 14],
[298, 92, 14],
[281, 94, 13],
[303, 93, 13],
[292, 98, 13],
[297, 94, 14],
[278, 99, 13],
[283, 76, 12],
[294, 92, 14],
[289, 84, 12],
[284, 90, 14],
[228, 84, 14],
])

Surface= np.array([

[306, 194, 56],
[139, 63, 14],
[241, 197, 56],
[0, 182, 51],
[194, 165, 47],
[166, 129, 39],
[177, 136, 39],
[0, 102, 31],
[267, 202, 53],
[172, 146, 36],
[294, 203, 54],
[272, 197, 54],
[218, 166, 44],
[142, 121, 34],
[170, 147, 34],
[106, 91, 24],
[231, 180, 47],
[248, 192, 53],
[244, 178, 49],
[208, 161, 46],
])

yellowMean = np.mean(Yellow, axis=0)
yellowStd = np.std(Yellow, axis=0)
purpleMean = np.mean(Purple, axis=0)
purpleStd = np.std(Purple, axis=0)
orangeMean = np.mean(Orange, axis=0)
orangeStd = np.std(Orange, axis=0)
surfaceMean = np.mean(Surface, axis=0)
surfaceStd = np.std(Surface, axis=0)
yellowMeanScaled = yellowMean/np.amax(yellowMean)*255
purpleMeanScaled = purpleMean/np.amax(purpleMean)*255
orangeMeanScaled = orangeMean/np.amax(orangeMean)*255
surfaceMeanScaled = surfaceMean/np.amax(surfaceMean)*255
print("Yellow Mean: ", yellowMeanScaled)
print("Yellow Std: ", yellowStd)
print("Purple Mean: ", purpleMeanScaled)
print("Purple Std: ", purpleStd)
print("Orange Mean: ", orangeMeanScaled)
print("Orange Std: ", orangeStd)
print("Surface Mean: ", surfaceMeanScaled)
print("Surface Std: ", surfaceStd)
