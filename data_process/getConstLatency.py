import sys
from utils import approximateConstLatency

exp_num = int(sys.argv[1])
set_num = int(sys.argv[2])

latency_val = approximateConstLatency(exp_num, set_num)
print(latency_val)