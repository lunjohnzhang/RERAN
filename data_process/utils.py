import numpy as np
import sys

def round_up(value):
	# replace round function to implement precise rounding of the 3rd digit
    return round(value * 1000) / 1000.0

def readReplayedTimePoint(file):
    try:
        timePointLines = open(file)
    except:
        print("file not found")
        sys.exit()
    lines = timePointLines.readlines()
    timePointBlocks = []
    j = 0
    while j < len(lines):
        line = lines[j]
        i = j
        if "Line Number" in line:
            timePoints = []
            i = int(line.split("=")[1].strip())
            j += 1
            count = 0
            while count < i:
                line = lines[j]
                j += 1
                if "time elapsed from" in line:
                    timePoints.append(int(line.split(":")[1].strip()))
                    count+=1
            timePointBlocks.append(timePoints)
        else:
            j += 1

    # print(timePointBlocks[0])
    return timePointBlocks

def readActualTimePoint(file):
    try:
        timePointLines = open(file)
    except:
        print("file not found")
        sys.exit()
    lines = timePointLines.readlines()
    timePointBlocks = []
    for line in lines:
        timePointBlocks.append(float(line.split(":")[1].strip()))
    return timePointBlocks

def takeDifference(replay, actual):
    difference = []
    for i, replayTP in enumerate(replay):
        difference.append(replayTP - actual[i])
    return difference