######
# readInData.py; readin replayData and store in array
# 
# 
#####
import sys
try:
    replay = open("exp2/replayTimeSet1.txt")
except:
    print("file not found")
    sys.exit()

lines = replay.readlines()
times = []
for line in lines:
    timeRaw = line.split("real")[0].strip()
    times.append(float(timeRaw)/12.512803)
print(times)