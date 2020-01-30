#######
# getMeanSdEro.py: calculate the time lapse of all events recorded, mean and standard diviation of all
# of the replay, and error of the above two
# argv[1]: recordedEvents.txt
# argv[2]: replayTimeSet.txt
#######

import math
import sys

# function to calculate the mean and standard diviation
def getMean(replayTimes):
	timeSum = sum(replayTimes)
	mean = timeSum / len(replayTimes)
	return mean

def getStandardDiviation(replayTimes):
	mean = getMean(replayTimes)
	total = 0.0
	for time in replayTimes:
		total += math.pow(time - mean, 2)
	sd = math.sqrt(total/len(replayTimes))
	return sd 

def round_up(value):
	# replace round function to implement precise rounding of the 3rd digit
    return round(value * 1000) / 1000.0

# read in recordedEvent and calculate the total time of the events recorded
recorded = open(sys.argv[1])
lines = recorded.readlines()
times = [] # array to store all of the times
for line in lines:
    if line[0] == "[":
        timeWithBraketAndSpace = line.split("]")
        timeWithBraket = timeWithBraketAndSpace[0].replace(" ", "")
        time = timeWithBraket.replace("[", "")
        times.append(float(time))

recordInterval = times[len(times) - 1] - times[0]
print("replay time is " + str(round_up(recordInterval)))

# read in all of the replaytime and calculate the mean and standard diviation
allReplay = open(sys.argv[2])
lines = allReplay.readlines()
replayTimes = []
for line in lines:
	line = line.replace(" ", "")
	time = line.split("real")[0]
	replayTimes.append(float(time))
replayMean = getMean(replayTimes)
replaySD = getStandardDiviation(replayTimes)
print("mean: " + str(round_up(replayMean)))
print("standard diviation: " + str(round_up(replaySD)))
print("error: " + str(round_up(replayMean / recordInterval)))
