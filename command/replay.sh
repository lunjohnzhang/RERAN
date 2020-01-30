DATA_P="data_process/"
SORTED_EVENTS="sortedEvents.txt"
TRANSLATED_EVENTS="translatedEvents.txt"
LOCAL_LATENCY_VALUE="localLatencyValue.txt"
PUSH_TO="data/local/"

SET="5"
SET_DIR="set"${SET}"/"
EXP="data_set/exp8/"${SET_DIR}

EXP_RECORDED_EVENTS=${EXP}"recordedEvents"${SET}".txt"

python ${DATA_P}sortEvents.py ${EXP_RECORDED_EVENTS} ${SORTED_EVENTS}
java bin/Translate ${SORTED_EVENTS} ${TRANSLATED_EVENTS}
adb push ${TRANSLATED_EVENTS} ${PUSH_TO}
adb push ${LOCAL_LATENCY_VALUE} ${PUSH_TO}

adb shell ${PUSH_TO}/./replay ${PUSH_TO}/${TRANSLATED_EVENTS} ${PUSH_TO}/${LOCAL_LATENCY_VALUE} 
