#######
# getActualIntervals.py: calculate the actual time interval in between each of the events in microseconds
# argv[1]: recordedEvents.txt
#######
import sys
from utils import round_up

recorded = open(sys.argv[1])
lines = recorded.readlines()
times = []  # array to store all of the times
for line in lines:
    if line[0] == "[":
        timeWithBraketAndSpace = line.split("]")
        timeWithBraket = timeWithBraketAndSpace[0].replace(" ", "")
        time = timeWithBraket.replace("[", "")
        times.append(float(time))

for i, time in enumerate(times):
    if i != 0:
        print("interval " + str(i) + ": " + str(round_up((times[i] - times[i-1])*1000000)))
        
