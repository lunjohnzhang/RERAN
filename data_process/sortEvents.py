import sys

def takeFirst(ele):
    return ele[0]

def main():
    fileIn = open(sys.argv[1], "r")
    fileOut = open("sortedEvents.txt", "w")
    data = []
    for line in fileIn:
        if(line[0] != "["):
           fileOut.write(line)
        else:
            lineTemp = line.replace("[", "")
            lineTemp = lineTemp.replace(" ", "")
            lineTemp = lineTemp.replace("]", "")
            lineSplited = lineTemp.split("/")
            timeStamp = lineSplited[0]
            data.append((timeStamp, line))
    data.sort(key = takeFirst)
    for ele in data:
        fileOut.write(ele[1])

if __name__ == "__main__" :
    main()
