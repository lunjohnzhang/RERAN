# Objective
In previous experiments we have figured out that there are lag time in replay. In this experiment, we tried different modifications to the algorithm to solve the lagging issue. At the same time, we want to have an idea about the lag constant of each loop.
1. Test if the latency function is a constant
2. try different fixs

# Modifications
## Brute Force Fix
Change sleeping time `toSleep` of each loop:
```c
toSleep = timeArray[j] - constant_latency_time
```

## Deficit Fix
Keep a deficit of lag time and keep up with as much time as possible during each loop.
```c
toSleep = timeArray[j] - constant_latency_time

// sleepDeficit is declared outside of event loop
if(toSleep < 0) {
	goSleep(0);
	sleepDeficit += 0 - toSleep;
}
else if (toSleep - sleepDeficit < 0) {
	goSleep(0);
	sleepDeficit -= sleepDeficit - toSleep;
}
else {
	goSleep(toSleep - sleepDeficit);
	sleepDeficit = 0;
}
```

## Sectional Deficit Fix:
Use precalculated latency time to calculate `toSleep`, and apply deficit method as usual
```c
toSleep = timeArray[j] - lLatency[j]*1000

// sleepDeficit is declared outside of event loop
if(toSleep < 0) {
	goSleep(0);
	sleepDeficit += 0 - toSleep;
}
else if (toSleep - sleepDeficit < 0) {
	goSleep(0);
	sleepDeficit -= sleepDeficit - toSleep;
}
else {
	goSleep(toSleep - sleepDeficit);
	sleepDeficit = 0;
}

### Important!!
Note that while running the test for sectional deficit, you need to use data_process/getLocalLatency.py to calculate the latency values. This part is not automatically included in the testing pipline. BE CAREFUL!!

```

# Data Sets
set1: Calculator app on samsumg S5 with brute force fix

set2: Calculator app on samsumg S5 with no fix

set3: Calculator app on samsumg S5 with deficit fix

set4: Calculator app on samsung S5 with sectional deficit fix