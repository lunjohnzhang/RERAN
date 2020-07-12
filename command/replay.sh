# command to replay specified workload once
source command/utils.sh

# preprocess recorded data and push to device
sort_events
translate_events
push_latency

# run replay agent
replay_with_latency
