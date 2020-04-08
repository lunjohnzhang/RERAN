# Note: This experiment is incomplete and the code probably contains bugs. Please do not trust the result until further notice.

# Objective
Test extreme sectional sleeping deficit method. Since the difference graph of normal sectional deficit method is not smooth, in this experiment, a modification to the original sectional deficit algorithm is made to try to smooth out the graph.

## Extreme Sectional Sleeping Deficit Method
Calculate record time points outside the loop. For each event loop, if the current timestamp is later than expected time point, execute current event immediately, else sleep.
```c
// outside loop:
uint64_t *timePoints;
timePoints = (uint64_t *)calloc((lineNumbers*1), sizeof(uint64_t));
timePoints[0] = timeArray[0];
for(i = 1; i < lineNumbers; ++i) {
    timePoints[i] = timePoints[i-1] + timeArray[i];
}

// inside loop:
toSleep = timeArray[j] - lLatency[j]*1000
if (toSleep < 0 || toSleep - sleepDeficit < 0) {
    // sleep only if current time is earlier than expected
    if(currTimePoint < timePoints[j]/1000.0) {
        goSleep(timePoints[j] - currTimePoint*1000);
    }

    // update deficit
    if(toSleep < 0) {
        sleepDeficit += 0 - toSleep;
    }
    else {
        sleepDeficit -= sleepDeficit - toSleep;
    }
}
else {
    goSleep(toSleep - sleepDeficit);
    sleepDeficit = 0;
}
```


# Data Set
set1: calculator app on samsung S5 taking latency of deficit code into account

set2: apply extreme sleeping deficit method to recordedEvents of set1

set3: apply normal sleeping deficit method to recordedEvents of set1

set4: apply max(toSleep, 0) method with extreme sleeping latency time

set5: apply extreme sleeping deficit method to recordedEvents of set1 with additional check of timepoint