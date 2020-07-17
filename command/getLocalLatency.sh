# command to run replay once and get local latency (difference of expected and actual time point) value
source command/utils.sh

# preprocess recorded data and push to device
sort_events
translate_events

# execute replay and log the replay time points (needs compiled replay.c to change accordingly)
replay_with_out_latency  > ${EXP_REPLAY_TIME_POINT}

# get actual time point
python ${DATA_P}getActualTimePoint.py ${EXP_RECORDED_EVENTS} > ${EXP_ACTUAL_TIME_POINT}

# get replay time point and calculate latency values
python ${DATA_P}getLocalLatency.py ${EXP_REPLAY_TIME_POINT} ${EXP_ACTUAL_TIME_POINT} > ${LOCAL_LATENCY_VALUE}
