#######
# getLocalLatency.py: approximate the local p value for each time point except the first one by calculating slope of every two ajacent points
# Formula: pi = ki = (yi - yi-1)/(xi - xi-1) = yi - yi-1
# argv[1]: replayTimePoint.txt
# argv[2]: actualTimePoint.txt
#######
import sys
import numpy as np
from utils import readReplayedTimePoint, readActualTimePoint, takeDifference

def approxLatency(difference):
    # calculate
    result = []
    for i in range(1, len(difference)):
        result.append(difference[i] - difference[i-1])
        # print("difference[i] - difference[i-1] = " + str(difference[i]) + " - " + str(difference[i-1]) + " = " + str(difference[i] - difference[i-1]))

    # print the result
    print(0) # make the number same as timeArray in replay.c
    for p in result:
        print(p)
    return result

replayTimePointsBlock = np.array(readReplayedTimePoint(sys.argv[1]))
actualTimePoints = np.array(readActualTimePoint(sys.argv[2]))

difference = np.zeros(actualTimePoints.shape[0])
for i in range(replayTimePointsBlock.shape[0]):
    difference += replayTimePointsBlock[i] - actualTimePoints
difference /= replayTimePointsBlock.shape[0]
approxLatency(difference)