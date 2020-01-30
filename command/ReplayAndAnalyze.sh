DATA_P="data_process/"
SORTED_EVENTS="sortedEvents.txt"
TRANSLATED_EVENTS="translatedEvents.txt"
LOCAL_LATENCY_VALUE="localLatencyValue.txt"
PUSH_TO="data/local/"

SET="5"
SET_DIR="set"${SET}"/"
EXP="data_set/exp8/"${SET_DIR}

EXP_RECORDED_EVENTS=${EXP}"recordedEvents"${SET}".txt"
EXP_REPLAY_TIME=${EXP}"replayTimeSet"${SET}".txt"
EXP_REPLAY_INTERVAL=${EXP}"replayIntervalSet"${SET}".txt"
EXP_ACTUAL_INTERVAL=${EXP}"actualIntervalSet"${SET}".txt"
EXP_REPLAY_TIME_POINT=${EXP}"replayTimePointSet"${SET}".txt"
EXP_ACTUAL_TIME_POINT=${EXP}"actualTimePointSet"${SET}".txt"


python ${DATA_P}sortEvents.py ${EXP_RECORDED_EVENTS} ${SORTED_EVENTS}
java bin/Translate ${SORTED_EVENTS} ${TRANSLATED_EVENTS}
adb push ${TRANSLATED_EVENTS} ${PUSH_TO}
adb push ${LOCAL_LATENCY_VALUE} ${PUSH_TO}
for ((i = 0; i < 20; i++));
do 
    2>>${EXP_REPLAY_TIME} time adb shell ${PUSH_TO}/./replay ${PUSH_TO}/${TRANSLATED_EVENTS} ${PUSH_TO}/${LOCAL_LATENCY_VALUE} >> ${EXP_REPLAY_TIME_POINT}; 
    sleep 3;
done
python ${DATA_P}getMeanSdEro.py ${EXP_RECORDED_EVENTS} ${EXP_REPLAY_TIME} >> ${EXP_REPLAY_TIME}
python ${DATA_P}getActualIntervals.py ${EXP_RECORDED_EVENTS} > ${EXP_ACTUAL_INTERVAL}
python ${DATA_P}getActualTimePoint.py ${EXP_RECORDED_EVENTS} > ${EXP_ACTUAL_TIME_POINT}
