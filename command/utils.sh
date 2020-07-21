# useful utils and variables

# path in repo
EXP=$1 # command args 1 is exp num
SET=$2 # command args 2 is set num
algo=$3 # command args 3 is algorithm type
        # Could be one of ["original", "bruteforce", "deficit", "sec_deficit"]
EXP_DIR="data_set/exp"${EXP}"/"
SET_DIR="set"${SET}"/"
EXP_SET_DIR=${EXP_DIR}${SET_DIR}

LOCAL_LATENCY_VALUE=${EXP_SET_DIR}"localLatencyValue.txt" # per event latency
CONST_LATENCY_VALUE=${EXP_SET_DIR}"constLatencyValue.txt" # const latency
TRANSLATED_EVENTS=${EXP_SET_DIR}"translatedEvents.txt"
SORTED_EVENTS=${EXP_SET_DIR}"sortedEvents.txt"

EXP_RECORDED_EVENTS=${EXP_SET_DIR}"recordedEvents"${SET}".txt"
EXP_REPLAY_TIME_POINT=${EXP_SET_DIR}"replayTimePointSet"${SET}".txt"
EXP_ACTUAL_TIME_POINT=${EXP_SET_DIR}"actualTimePointSet"${SET}".txt"
EXP_REPLAY_TIME=${EXP_SET_DIR}"replayTimeSet"${SET}".txt"
EXP_REPLAY_INTERVAL=${EXP_SET_DIR}"replayIntervalSet"${SET}".txt"
EXP_ACTUAL_INTERVAL=${EXP_SET_DIR}"actualIntervalSet"${SET}".txt"

# path on device
DATA_P="data_process/"
PUSH_TO="data/local/"
PUSHED_TRANSLATE=${PUSH_TO}"translatedEvents.txt"
PUSHED_LATENCY=${PUSH_TO}"localLatencyValue.txt"

# util functions
function sort_events {
    python ${DATA_P}sortEvents.py ${EXP_RECORDED_EVENTS} > ${SORTED_EVENTS}
}

function approximate_const_latency {
    python ${DATA_P}getConstLatency.py ${EXP} ${SET}
}

function approximate_perevent_latency {
    python ${DATA_P}getLocalLatency.py ${EXP_REPLAY_TIME_POINT} ${EXP_ACTUAL_TIME_POINT}
}

function get_actual_time_pt {
    python ${DATA_P}getActualTimePoint.py ${EXP_RECORDED_EVENTS}
}

function translate_events {
    java bin/Translate ${SORTED_EVENTS} ${TRANSLATED_EVENTS}
    adb push ${TRANSLATED_EVENTS} ${PUSH_TO}
}

function push_latency {
    adb push ${LOCAL_LATENCY_VALUE} ${PUSH_TO}
}

function read_in_const_latency {
    line=$(head -n 1 $CONST_LATENCY_VALUE)
    echo $line
}

# function replay_with_out_latency {
#     adb shell ${PUSH_TO}/./replay ${PUSHED_TRANSLATE}
# }

# function replay_with_latency {
#     # adb shell ${PUSH_TO}/./replay ${PUSHED_TRANSLATE} ${PUSHED_LATENCY}
#     # adb shell data/local/./replay -t data/local/translatedEvents.txt -a bruteforce -l data/local/localLatencyValue.txt
#     adb shell data/local/./replay -t data/local/translatedEvents.txt -a bruteforce -l 200.0
# }

# function to execute replay
# Args:
#   algo(string): which scheduler algorithm to run.
#   latency: filename of the latency values or a const latency value
function replay {
    algo=$1
    if [ "$algo" == "original" ]; then
        2>>${EXP_REPLAY_TIME} time adb shell ${PUSH_TO}/./replay -t ${PUSHED_TRANSLATE} -a "original"
    fi

    if [ "$algo" == "bruteforce" ]; then
        latency_val=$(read_in_const_latency) # get const latency value
        2>>${EXP_REPLAY_TIME} time adb shell ${PUSH_TO}/./replay -t ${PUSHED_TRANSLATE} -a "bruteforce" -l latency_val
    fi

    if [ "$algo" == "deficit" ]; then
        latency_val=$(read_in_const_latency) # get const latency value
        2>>${EXP_REPLAY_TIME} time adb shell ${PUSH_TO}/./replay -t ${PUSHED_TRANSLATE} -a "deficit" -l latency_val
    fi

    if [ "$algo" == "sec_deficit" ]; then
        2>>${EXP_REPLAY_TIME} time adb shell ${PUSH_TO}/./replay -t ${PUSHED_TRANSLATE} -a "sec_deficit" -l ${PUSHED_LATENCY}
    fi
}