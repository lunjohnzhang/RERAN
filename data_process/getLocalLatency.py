#######
# getLocalLatency.py: approximate the local p value for each time point except the first one by calculating slope two each of the two ajacent points
# Formula: pi = ki = (yi - yi-1)/(xi - xi-1) = yi - yi-1
# argv[1]: replayTimePoint.txt
# argv[2]: actualTimePoint.txt
#######
import sys

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
    # print(len(timePointBlocks))
    # print(timePointBlocks)
    return timePointBlocks

def takeDifference(replay, actual):
    difference = []
    for i, replayTP in enumerate(replay):
        difference.append(replayTP - actual[i])
        # print("replay" + "[" + str(i) + "]" + " - actual" + "[" + str(i) + "]" + " = " + str(replayTP) + " - " + str(actual[i]) + " = " + str(replayTP - actual[i]))
    return difference

def approxLatency(difference):
    # calculate
    result = []
    for i in range(1, len(difference)):
        result.append(difference[i] - difference[i-1])
        # print("difference[i] - difference[i-1] = " + str(difference[i]) + " - " + str(difference[i-1]) + " = " + str(difference[i] - difference[i-1]))
    
    # print the result
    for p in result:
        print(p)
    return result

replayTimePointsBlock = readReplayedTimePoint(sys.argv[1])
actualTimePoints = readActualTimePoint(sys.argv[2])
difference = takeDifference(replayTimePointsBlock[0], actualTimePoints)
approxLatency(difference)