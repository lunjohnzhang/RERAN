DATA_P="data_process/"
LOCAL_LATENCY_VALUE="localLatencyValue.txt"
PUSH_TO="data/local/"

SET="1"
SET_DIR="set"${SET}"/"
EXP="data_set/exp8/"${SET_DIR}

EXP_RECORDED_EVENTS=${EXP}"recordedEvents"${SET}".txt"
EXP_REPLAY_TIME_POINT=${EXP}"replayTimePointSet"${SET}".txt"
EXP_ACTUAL_TIME_POINT=${EXP}"actualTimePointSet"${SET}".txt"

python ${DATA_P}getLocalLatency.py ${EXP_REPLAY_TIME_POINT} ${EXP_ACTUAL_TIME_POINT} > ${LOCAL_LATENCY_VALUE}
