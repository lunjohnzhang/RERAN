~/Desktop/Coding/Android/ndk-arm/bin/arm-linux-androideabi-clang -pie src/replay.c -o bin/replay
adb push bin/replay data/local/