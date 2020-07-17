import os
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

REPLAY_TIME_PT_PATH = "data_set/exp%d/set%d/replayTimePointSet%d.txt"
ACTUAL_TIME_PT_PATH = "data_set/exp%d/set%d/actualTimePointSet%d.txt"


def round_up(value):
    # replace round function to implement precise rounding of the 3rd digit
    return round(value * 1000) / 1000.0


def readReplayedTimePoint(file):
    """Read in "replayTimePointSet{x}.txt"
    """
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
                    count += 1
            timePointBlocks.append(timePoints)
        else:
            j += 1

    return timePointBlocks


def readActualTimePoint(file):
    """Read in "actualTimePointSet{x}.txt"
    """
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
    return np.array(replay) - np.array(actual)


def getErrorPearson(difference):
    """Apply Pearson test to input array to test linearity of the dataset
    """
    x = []
    for i in range(0, len(difference)):
        x.append(i)
    corr, p_value = pearsonr(x, difference)
    return corr

##### Linear Regression #####
def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return(b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m", marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


def construct_x(n):
    result = []
    for i in range(0, n):
        result.append(i)
    return result


def linear_regression(y_difference, n):
    # observations
    x = np.array(construct_x(n))
    y = np.array(y_difference)

    # estimating coefficients
    b = estimate_coef(x, y)
    error = getErrorPearson(y_difference)
    print("Estimated coefficients:\n b_0 = {} \n b_1 = {}".format(b[0], b[1]))
    print("Pearson error: " + str(error))
    # plotting regression line
    plot_regression_line(x, y, b)
    return [b[0], b[1], error]


def plot_regression_line_multi(x1, y1, b_a, x2, y2, b_b):
    # plotting the actual points as scatter plot
    plt.scatter(x1, y1, color="b", marker="o", s=30, label="before fix")  # old
    plt.scatter(x2, y2, color="r", marker="o", s=30, label="after fix")  # new

    # predicted response vector
    y_pred1 = b_a[0] + b_a[1]*x1
    y_pred2 = b_b[0] + b_b[1]*x2

    # plotting the regression line
    plt.plot(x1, y_pred1, color="g")
    plt.plot(x2, y_pred2, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.legend()
    plt.show()


def linear_regression_multi(y_difference1, n1, y_difference2, n2):
    # observations
    x1 = np.array(construct_x(n1))
    y1 = np.array(y_difference1)

    x2 = np.array(construct_x(n2))
    y2 = np.array(y_difference2)

    # estimating coefficients
    b_a = estimate_coef(x1, y1)
    b_b = estimate_coef(x2, y2)
    print("Before fixing: ")
    print("Estimated coefficients:\n b_0_old = {} \n b_1_old = {}".format(
        b_a[0], b_a[1]))
    print("Pearson error: " + str(getErrorPearson(y_difference1)))
    print("\nAfter fixing: ")
    print("Estimated coefficients:\n b_0_new = {} \n b_1_new = {}".format(
        b_b[0], b_b[1]))
    print("Pearson error: " + str(getErrorPearson(y_difference2)))
    # plotting regression line
    plot_regression_line_multi(x1, y1, b_a, x2, y2, b_b)

######End of Linear Regression ######


def plotRecordActualCom(exp_num, set_num):
    """Plot recorded and replayed time points
    """
    replayTimePointsBlock = readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num, set_num, set_num))
    actualTimePoints = readActualTimePoint(
        ACTUAL_TIME_PT_PATH % (exp_num, set_num, set_num))

    plt.axis([0, 351, 0, 1.5e7])
    plt.plot(replayTimePointsBlock[0], 'ro', label="replay")
    plt.plot(actualTimePoints, 'bo', label="actual")
    plt.legend()
    plt.show()


def plotRecordActualDiff(exp_num, set_num, color='ro', label=None, axis=[0, 426, 0, 0.6*1e7]):
    """Plot difference curve of recorded and replayed time points
    """
    replayTimePointsBlock = np.array(readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num, set_num, set_num)))
    actualTimePoints = np.array(readActualTimePoint(
        ACTUAL_TIME_PT_PATH % (exp_num, set_num, set_num)))

    # take the average difference between the record and 20 replays
    num = replayTimePointsBlock.shape[0]
    difference = np.zeros(actualTimePoints.shape[0])
    for i in range(num):
        difference += np.array(takeDifference(
            replayTimePointsBlock[i], actualTimePoints))
    difference /= num
    plt.axis([0, 426, 0, 0.6*1e7])
    plt.plot(difference, color, label=label)


def plotFixComWithLR(exp_num_before, set_num_before, exp_num_after, set_num_after):
    """
    Plot two sets of recorded and replayed time points
    with linear regression applied to compare performance
    """
    replayTimePointsBlock = readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num_before, set_num_before, set_num_before))
    actualTimePoints = readActualTimePoint(ACTUAL_TIME_PT_PATH % (
        exp_num_before, set_num_before, set_num_before))
    difference = takeDifference(replayTimePointsBlock[0], actualTimePoints)

    replayTimePointsBlock = readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num_after, set_num_after, set_num_after))
    actualTimePoints = readActualTimePoint(
        ACTUAL_TIME_PT_PATH % (exp_num_after, set_num_after, set_num_after))
    difference_exp = takeDifference(replayTimePointsBlock[0], actualTimePoints)

    linear_regression_multi(difference, len(difference),
                            difference_exp, len(difference_exp))
