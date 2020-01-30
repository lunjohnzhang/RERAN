SET_DIR="set"${SET}"/"
EXP="data_set/exp8/"${SET_DIR}
EXP_RECORDED_EVENTS=${EXP}"recordedEvents"${SET}".txt"

adb shell getevent -tt > ${EXP_RECORDED_EVENTS}