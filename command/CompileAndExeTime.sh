~/Desktop/Coding/Android/ndk-arm/bin/arm-linux-androideabi-clang -pie data_set/exp6/time.c -o data_set/exp6/time_Android
adb push data_set/exp6/time_Android data/local/
adb shell time data/local/./time_Android > data_set/exp6/timeOutput.txt