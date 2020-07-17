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
    return np.arange(n)


def linear_regression(y_difference, n, log=True, plot=True):
    """python application of linear regression

    Args:
        y_difference: array of y values
        n: number of values in y

    Note: I am too lazy to change this to more mature ML packages
    """
    # observations
    x = np.array(construct_x(n))
    y = np.array(y_difference)

    # estimating coefficients
    b = estimate_coef(x, y)
    error = getErrorPearson(y_difference)

    # log result
    if log:
        print("Estimated coefficients:\n b_0 = {} \n b_1 = {}".format(b[0], b[1]))
        print("Pearson error: " + str(error))

    # plotting regression line
    if plot:
        plot_regression_line(x, y, b)
    return [b[0], b[1], error]


def plot_regression_line_multi(x1, y1, param1, x2, y2, param2):
    """Plot two regression lines

    Note: for a line y=kx+b: param[0] = b, param[1] = k
    """
    # plotting the actual points as scatter plot
    plt.scatter(x1, y1, color="b", marker="o", s=30, label="before fix")  # old
    plt.scatter(x2, y2, color="r", marker="o", s=30, label="after fix")  # new

    # predicted response vector
    y_pred1 = param1[0] + param1[1]*x1
    y_pred2 = param2[0] + param2[1]*x2

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
    param1 = estimate_coef(x1, y1)
    param2 = estimate_coef(x2, y2)
    print("Before fixing: ")
    print("Estimated coefficients:\n b_0_old = {} \n b_1_old = {}".format(
        param1[0], param1[1]))
    print("Pearson error: " + str(getErrorPearson(y_difference1)))
    print("\nAfter fixing: ")
    print("Estimated coefficients:\n b_0_new = {} \n b_1_new = {}".format(
        param2[0], param2[1]))
    print("Pearson error: " + str(getErrorPearson(y_difference2)))
    # plotting regression line
    plot_regression_line_multi(x1, y1, param1, x2, y2, param2)

######End of Linear Regression ######


def getRecordReplayDiff(exp_num, set_num):
    """Get record-replay-diff curve.
       Read in recorded and replayed time points, and take the difference.
    """
    replayTimePointsBlock = np.array(readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num, set_num, set_num)))
    actualTimePoints = np.array(readActualTimePoint(
        ACTUAL_TIME_PT_PATH % (exp_num, set_num, set_num)))

    # take the average difference between the record and replays
    num_replay = replayTimePointsBlock.shape[0]
    difference = np.zeros(actualTimePoints.shape[0])
    for i in range(num_replay):
        difference += np.array(takeDifference(
            replayTimePointsBlock[i], actualTimePoints))
    difference /= num_replay
    return difference

def approximateConstLatency(exp_num, set_num):
    """Approximate constant latency value by applying
       linear regression record-replay-diff curve.

       return: approximated latency value in microseconds
    """
    difference = getRecordReplayDiff(exp_num, set_num)
    _, k, _ = linear_regression(difference, len(difference), log=False, plot=False)
    return round(k)

def plotRecordActualCom(exp_num, set_num, axis=[0, 351, 0, 1.5e7]):
    """Plot recorded and replayed time points
    """
    replayTimePointsBlock = readReplayedTimePoint(
        REPLAY_TIME_PT_PATH % (exp_num, set_num, set_num))
    actualTimePoints = readActualTimePoint(
        ACTUAL_TIME_PT_PATH % (exp_num, set_num, set_num))

    plt.axis(axis)
    plt.plot(replayTimePointsBlock[0], 'ro', label="replay")
    plt.plot(actualTimePoints, 'bo', label="actual")
    plt.legend()
    plt.show()


def plotRecordActualDiff(exp_num, set_num, color='ro', label=None, axis=[0, 426, 0, 0.6*1e7]):
    """Plot difference curve of recorded and replayed time points
    """
    difference = getRecordReplayDiff(exp_num, set_num)
    plt.axis(axis)
    plt.plot(difference, color, label=label)


def plotFixComWithLR(exp_num_before, set_num_before, exp_num_after, set_num_after):
    """
    Plot two sets of recorded and replayed time points
    with linear regression applied to compare performance
    """
    diff_before = getRecordReplayDiff(exp_num_before, set_num_before)
    diff_after = getRecordReplayDiff(exp_num_after, set_num_after)

    linear_regression_multi(diff_before, len(diff_before),
                            diff_after, len(diff_after))
