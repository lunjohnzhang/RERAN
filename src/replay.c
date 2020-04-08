/*
Copyright (c) 2011-2013, Lorenzo Gomez (lorenzobgomez@gmail.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of 
conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list 
of conditions and the following disclaimer in the documentation and/or other materials 
provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <time.h>
#include <inttypes.h>
// #include <sys/timeb.h> /* ftime, timeb (for timestamp in millisecond) */
// #include <sys/time.h>  /* gettimeofday, timeval (for timestamp in microsecond) */

struct input_event {
	struct timeval time;
	unsigned short type;
	unsigned short code;
	unsigned long value;
};


void goSleep(uint64_t nsec)
{
	struct timespec timeout0;
	struct timespec timeout1;
	struct timespec* tmp;
	struct timespec* t0 = &timeout0;
	struct timespec* t1 = &timeout1;

	t0->tv_sec = (long)(nsec / 1000000000);
	t0->tv_nsec = (long)(nsec % 1000000000);
	
	//printf("Sleeping for %lu sec, %lu nsec\n", t0->tv_sec, t0->tv_nsec);

	while ((nanosleep(t0, t1) == (-1)) && (errno == EINTR))
	{
		tmp = t0;
		t0 = t1;
		t1 = tmp;
	}
}

// from <linux/input.h>
#define EVIOCGVERSION		_IOR('E', 0x01, int)			/* get driver version */
#define EVIOCGID		_IOR('E', 0x02, struct input_id)	/* get device ID */
#define EVIOCGKEYCODE		_IOR('E', 0x04, int[2])			/* get keycode */
#define EVIOCSKEYCODE		_IOW('E', 0x04, int[2])			/* set keycode */

#define EVIOCGNAME(len)		_IOC(_IOC_READ, 'E', 0x06, len)		/* get device name */
#define EVIOCGPHYS(len)		_IOC(_IOC_READ, 'E', 0x07, len)		/* get physical location */
#define EVIOCGUNIQ(len)		_IOC(_IOC_READ, 'E', 0x08, len)		/* get unique identifier */

#define EVIOCGKEY(len)		_IOC(_IOC_READ, 'E', 0x18, len)		/* get global keystate */
#define EVIOCGLED(len)		_IOC(_IOC_READ, 'E', 0x19, len)		/* get all LEDs */
#define EVIOCGSND(len)		_IOC(_IOC_READ, 'E', 0x1a, len)		/* get all sounds status */
#define EVIOCGSW(len)		_IOC(_IOC_READ, 'E', 0x1b, len)		/* get all switch states */

#define EVIOCGBIT(ev,len)	_IOC(_IOC_READ, 'E', 0x20 + ev, len)	/* get event bits */
#define EVIOCGABS(abs)		_IOR('E', 0x40 + abs, struct input_absinfo)		/* get abs value/limits */
#define EVIOCSABS(abs)		_IOW('E', 0xc0 + abs, struct input_absinfo)		/* set abs value/limits */

#define EVIOCSFF		_IOC(_IOC_WRITE, 'E', 0x80, sizeof(struct ff_effect))	/* send a force effect to a force feedback device */
#define EVIOCRMFF		_IOW('E', 0x81, int)			/* Erase a force effect */
#define EVIOCGEFFECTS		_IOR('E', 0x84, int)			/* Report number of effects playable at the same time */

#define EVIOCGRAB		_IOW('E', 0x90, int)			/* Grab/Release device */

// end <linux/input.h>

#define ARRAYSIZE(x)  (sizeof(x)/sizeof(*(x)))
 

int main(int argc, char *argv[])
{
		
	if(argc == 1)
	{
		printf("ERROR: Please specify the location of the event file\n\n");
		exit(1);
	}
	
	int returned = 0;
	long lineNumbers = 0;


	FILE *fl = fopen(argv[2], "r"); // localLatency.txt
	FILE *file = fopen(argv[1], "r"); // translatedEvents.txt
	
	if(file && fl)
	{

		size_t i, j, k, l, m, x;
		
		char buffer[BUFSIZ], *ptr;
		fgets(buffer, sizeof buffer, file);
		ptr = buffer;
		lineNumbers = (long)strtol(ptr, &ptr, 10);
		
		printf("\n\nLine Numbers = %lu\n\n", lineNumbers);
		

		// ************************************************
		// read in local latency
		int64_t *lLatency;
		lLatency = (int64_t*) calloc((lineNumbers*1), sizeof(int64_t));
		lLatency[0] = 0;
		char line[255];
		char *ptr_;
		for(int i=1; i<lineNumbers; i++) {
			fscanf(fl, "%s", line);
			// printf("%d: %s\n", i, line );
			ptr_ = line;
			lLatency[i] = strtoll(ptr_, &ptr_, 10);
		}
		// ************************************************


		// eventType will then match based on whatever is in the sendEvents.txt file
		unsigned short * eventType;
		unsigned short * codeData;
		unsigned short * typeData;
		unsigned long * valueData;
		uint64_t * timeArray;
		
		eventType = (unsigned short *) calloc((lineNumbers*1), sizeof(unsigned short));
		codeData = (unsigned short *) calloc((lineNumbers*1), sizeof(unsigned short));
		typeData = (unsigned short *) calloc((lineNumbers*1), sizeof(unsigned short));		
		valueData = (unsigned long *) calloc((lineNumbers*1), sizeof(unsigned long));
		timeArray = (uint64_t *) calloc((lineNumbers*1), sizeof(uint64_t));
		
	
		if(eventType == NULL)
			printf("eventType failed malloc\n");
		if(codeData == NULL)
			printf("codeData failed malloc\n");
		if(typeData == NULL)
			printf("typeData failed malloc\n");
		if(valueData == NULL)
			printf("valueData failed malloc\n");
		if(timeArray == NULL)
			printf("timeArray failed malloc\n");
	
		
		int everyOther = 0;
	
		for(i = 0, l = 0, m = 0; fgets(buffer, sizeof buffer, file); ++i)
		{
			if(everyOther == 1)
			{
				for(j = 0, ptr = buffer; j < 4; ++j, ++ptr)
				{
					if(j == 0)
						eventType[m] = (unsigned short)strtoul(ptr, &ptr, 10);						
					else if(j == 1)
						codeData[m] = (unsigned short)strtoul(ptr, &ptr, 10);
					else if(j == 2)
						typeData[m] = (unsigned short)strtoul(ptr, &ptr, 10);
					else if(j == 3)
						valueData[m] = (unsigned long)strtoul(ptr, &ptr, 10);					
				}
				
				m++;
				everyOther = 0;					
			}
			else
			{
				ptr = buffer;
				timeArray[l] = (uint64_t)strtoull(ptr, &ptr, 10);		
				everyOther = 1;
				l++;
			}
		}
		fclose(file);

		// *******************************************************************
		// find timepoints using time interval in timeArray
		uint64_t *timePoints;
		timePoints = (uint64_t *)calloc((lineNumbers*1), sizeof(uint64_t));
		timePoints[0] = timeArray[0];
		for(i = 1; i < lineNumbers; ++i) {
			timePoints[i] = timePoints[i-1] + timeArray[i];
			// printf("time point%zd: %lld\n", i, timePoints[i]);
		}

		// *******************************************************************
		

		//========		Start Sending Events		============

		char device[] = "/dev/input/event    ";
		char *start = device + 16;
		//[16-19] is for the event input number

		char* deviceP = device;
		int fd;
		
		j=0,k=0;
		// *******************************************************************
		// variables needed for interval calculation
		long long int prevMicros;
		long long int micros;
		int firstLoop = 1;

		// variables needed for time point calculation
		long long int initTimePoint;
		int firstLoop_tp = 1;
		long long int currTimePoint; // used for determining whether current time is before expected time point
		struct timeval currTime;

		// variables needed for testing whether lantency function is constant
		int64_t toSleep = 0;
		int64_t sleepDeficit = 0;

		// variable needed to sectional deficit solution
		// ********************************************************************


		// For each of the line numbers get the event, validate it, and then write it
		while (k < lineNumbers)
		{
			if (eventType[k] > 9999)
			{
				fprintf(stderr, "could not handle so many types of events.\n");
				return 1;
			}
			sprintf(start, "%d", eventType[k]);
			fd = open(deviceP, O_RDWR); // system call: open the file /dev/input/event#

			int ret; // can be moved out
			int version; // can be moved out
		
			// Make sure opening the device opens properly
			if(fd <= 0)
			{
				fprintf(stderr, "could not open %s, %s\n", *(&deviceP), strerror(errno));
				return 1;
			}
			
			// system call: get the version of the driver of the device
			// since need to check for every event file, not able to optimize
			if (ioctl(fd, EVIOCGVERSION, &version)) 
			{
				fprintf(stderr, "could not get driver version for %s, %s\n", *(&deviceP), strerror(errno));
				return 1;
			}
			
			struct input_event checkEvent[5];
			int valid = 0;			
			
			// need discussion: 
			// if the time interval of two events is less than 10^-6, adb getevent tool would think of them as they happens at the same time.
			// Therefore, the following code is detecting these events, write them together, and avoid sleeping.

			if(timeArray[j] == 0)
			{
				// Prep the event for checking, store the type, code, value in checkEvent
				l = 0;
				while((timeArray[j] == 0) && (j < lineNumbers)) //check the next one, but not if at end of array
				{
					checkEvent[l].type = codeData[k];
					checkEvent[l].code = typeData[k];
					checkEvent[l].value = valueData[k];
					j++;
					k++;
					l++;
					valid++;
				}
			}
			else
			{
				// Sleep for time interval calculated in Translate
				//printf("%d. ", k);
				// goSleep(timeArray[j]);

				// *****************************************************************************
				// experiment: sleep for less time than orginally required
				// toSleep = timeArray[j] - 17516380;
				// // printf("To sleep: %lld \n", toSleep);
				// // if current sleeping time is smaller than 0, add the extra sleeping time to deficit
				// if(toSleep < 0) {
				// 	goSleep(0);
				// 	sleepDeficit += 0 - toSleep;
				// }
				// else if (toSleep - sleepDeficit < 0) {
				// 	goSleep(0);
				// 	sleepDeficit -= sleepDeficit - toSleep;
				// }
				// else {
				// 	goSleep(toSleep - sleepDeficit);
				// 	sleepDeficit = 0;
				// }
				// *****************************************************************************
				// normal/extreme sectional sleeping deficit method
				// toSleep = timeArray[j] - 15880768;
				// printf("j = %zd k = %zd\n", j, k);
				// printf("current latency: %lld\n", lLatency[j]);
				
				toSleep = timeArray[j] - lLatency[j]*1000;
				
				// printf("timeArray[%zd] - p%zd = %lld - %lld = %lld\n", j, j, timeArray[j], lLatency[j]*1000, timeArray[j] - lLatency[j]*1000);
				// printf("current toSleep: %lld\n", toSleep);
				// if(toSleep > 0) {
				// 	goSleep(toSleep);
				// }
				// else{
				// 	goSleep(0);
				// }

				// get current time from start
				if (!gettimeofday(&currTime, NULL))
				{
					currTimePoint = ((long long int)currTime.tv_sec) * 1000000ll + (long long int)currTime.tv_usec;
				}
				// **************************
				if (toSleep < 0 || toSleep - sleepDeficit < 0) {
					if(currTimePoint >= timePoints[j]/1000.0) {
						goSleep(0);
					}
					else {
						goSleep(timePoints[j] - currTimePoint*1000);
					}
					if(toSleep < 0) {
						sleepDeficit += 0 - toSleep;
					}
					else {
						sleepDeficit -= sleepDeficit - toSleep;
					}
				}
				// else if (toSleep - sleepDeficit < 0) {
				// 	if (currTimePoint >= timePoints[j]) {
				// 		goSleep(0);
				// 	}
				// 	else {
				// 		goSleep(timePoints[j] - currTimePoint);
				// 	}
					
				// }
				else {
					goSleep(toSleep - sleepDeficit);
					sleepDeficit = 0;
				}
				// printf("current deficit: %lld nanoseconds\n", sleepDeficit);

				// *****************************************************************************	
				checkEvent[0].type = codeData[k];
				checkEvent[0].code = typeData[k];
				checkEvent[0].value = valueData[k];
				j++;
				k++;
				valid = 1;
			}
			
			struct input_event event[valid];
			memset(&event, 0, sizeof(event));
			
			for(x = 0; x < valid; x++)
			{
				event[x].type = checkEvent[x].type;
				event[x].code = checkEvent[x].code;
				event[x].value = checkEvent[x].value;
			}
					
			// get the current timeStamp and calculate the time interval by microseconds
			/* Example of timestamp in microsecond. */
			// struct timeval timer_usec;
			// long long int timestamp_usec; /* timestamp in microsecond */
			// if (!gettimeofday(&timer_usec, NULL))
			// {
			// 	timestamp_usec = ((long long int)timer_usec.tv_sec) * 1000000ll +
			// 					 (long long int)timer_usec.tv_usec;
			// }
			// else
			// {
			// 	timestamp_usec = -1;
			// }
			// micros = timestamp_usec;
			// if (firstLoop == 1)
			// {
			// 	firstLoop = 0;
			// 	prevMicros = micros;
			// }
			// else
			// {
			// 	// printf("microseconds: %lld \n", micros - prevMicros);
			// 	prevMicros = micros;
			// }
			

			// struct timespec tms;
			// if (clock_gettime(CLOCK_REALTIME, &tms))
			// {
			// 	return -1;
			// }
			// /* seconds, multiplied with 1 billion */
			// micros = tms.tv_sec * 1000000000;
			// /* Add full microseconds */
			// micros += tms.tv_nsec;
			// if(firstLoop == 1){
			// 	firstLoop = 0;
			// 	prevMicros = micros;
			// }
			// else{
			// 	printf("microseconds: %" PRId64 "\n", micros-prevMicros);
			// 	prevMicros = micros;
			// }

			// get time point
			// ***************************************************************
			// profile the following code
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
			if(firstLoop_tp == 1) {
				initTimePoint = timestamp_usec_tp;
				firstLoop_tp = 0;
				printf("time elapsed from t0: %d \n\n", 0); // microseconds
			}
			else {
				printf("time elapsed from t0: %lld \n\n", timestamp_usec_tp - initTimePoint); // microseconds
			}
			// ***************************************************************

			// ** Write the event that we just got from checkEvent **
			ret = write(fd, &event, sizeof(event));

			if(ret < sizeof(event))
			{
				fprintf(stderr, "write event failed, %s\n", strerror(errno));
				//should exit...
			}
			close(fd);
		}
	}
	else // fopen() returned NULL
	{
		//perror(filename);
		perror(argv[1]);
	}
	
	return 0;
}

