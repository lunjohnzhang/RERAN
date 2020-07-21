# command to run replay once and get local latency (difference of expected and actual time point) value
source command/utils.sh

# preprocess recorded data and push to device
sort_events
translate_events

# execute replay with original algo and log the replay time pointss
replay "original"  > ${EXP_REPLAY_TIME_POINT}

# get actual time point
get_actual_time_pt > ${EXP_ACTUAL_TIME_POINT}

# calculate constant latency value
approximate_const_latency > ${CONST_LATENCY_VALUE}

# calculate per event latency values
approximate_perevent_latency > ${LOCAL_LATENCY_VALUE}
