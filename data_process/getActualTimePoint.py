#######
# getActualTimePoint.py: calculate the actual time point (how much time has elapsed from the point where the first event started)
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
        print("point " + str(i) + ": " + str(round_up((times[i] - times[0])*1000000)))
    else:
        print("point 0: 0.0")