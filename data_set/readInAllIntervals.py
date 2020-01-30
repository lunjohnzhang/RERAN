######
# readInAllIntervals.py; readin replayed interval and actual interval
# argv[1]: replayIntervalSet.txt
# argv[2]: actualIntervalSet.txt
#####

##########
# read in replayed intervals
import sys
def readReplayedInterval():
    try:
        intervalLines = open("exp4/set3/replayIntervalSet3.txt")
    except:
        print("file not found")
        sys.exit()
    lines = intervalLines.readlines()
    intervalBlocks = []
    j = 0
    while j < len(lines):
        line = lines[j]
        i = j
        if "Line Number" in line:
            intervals = []
            i += int(line.split("=")[1].strip())
            j += 1
            # count = 0
            while j < i:
                line = lines[j]
                if "microseconds" in line:
                    intervals.append(int(line.split(":")[1].strip()))
                j += 1
            intervalBlocks.append(intervals)
        else:
            j += 1

    print(intervalBlocks)
    return intervalBlocks


# end of read in replayed intervals
##########
# read in actual interval
def readActualInterval():
    try:
        intervalLines = open("exp4/set3/actualIntervalSet3.txt")
    except:
        print("file not found")
        sys.exit()
    lines = intervalLines.readlines()
    intervals = []
    for line in lines:
        intervals.append(float(line.split(":")[1].strip()))
    print(intervals)
    return intervals

intervals = readActualInterval()