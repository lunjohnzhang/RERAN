#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>

int main() {
    // result: 54 microseconds
    long long int initTimePoint;
    int firstLoop_tp = 1;
    
    for(long long int i = 0; i < 100000; i++)
    {
        // variables needed for time point calculation
        struct timeval timer_usec_tp;
        long long int timestamp_usec_tp; /* timestamp in microsecond */
        if (!gettimeofday(&timer_usec_tp, NULL))
        {
            timestamp_usec_tp = ((long long int)timer_usec_tp.tv_sec) * 1000000ll +
                                (long long int)timer_usec_tp.tv_usec;
        }
        else
        {
            timestamp_usec_tp = -1;
        }
        if (firstLoop_tp == 1)
        {
            initTimePoint = timestamp_usec_tp;
            firstLoop_tp = 0;
        }
        else
        {
            printf("time elapsed from t1: %lld \n", timestamp_usec_tp - initTimePoint);
        }
    }
    return 0;
}

