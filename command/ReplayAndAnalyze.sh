# command to run replay for a certain number times, record the data, and do analysis
source command/utils.sh

sort_events
translate_events
push_latency
for ((i = 0; i < 1; i++));
do
    replay $algo > ${EXP_REPLAY_TIME_POINT}
    sleep 3;
done
# python ${DATA_P}getMeanSdEro.py ${EXP_RECORDED_EVENTS} ${EXP_REPLAY_TIME} >> ${EXP_REPLAY_TIME}
# python ${DATA_P}getActualIntervals.py ${EXP_RECORDED_EVENTS} > ${EXP_ACTUAL_INTERVAL}
# python ${DATA_P}getActualTimePoint.py ${EXP_RECORDED_EVENTS} > ${EXP_ACTUAL_TIME_POINT}
