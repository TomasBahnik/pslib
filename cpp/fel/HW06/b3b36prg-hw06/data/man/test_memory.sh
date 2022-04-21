#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TIMING_FORMAT='+%s.%N'
function timing() {
  printf "%s : %s sec\n" "$1" "$(date $TIMING_FORMAT)"
}

HW=06
OUTPUT_FILE="b3b36prg-hw$HW"
COMPILE_FILES="../../queue.c ../../main.c"
message "remove file '$OUTPUT_FILE'"
rm -f $OUTPUT_FILE
CLANG_OPTIONS="-pedantic -Wall -Werror -std=c99 -O3 -lm"
message "compiling with 'clang $CLANG_OPTIONS $COMPILE_FILES -o $OUTPUT_FILE'"
clang $CLANG_OPTIONS $COMPILE_FILES -o $OUTPUT_FILE

TEST_FILES=(pub*.in)
test_file=${TEST_FILES[0]}
VALGRIND_OPTIONS="--leak-check=full --leak-resolution=med --track-origins=yes --vgdb=no"
message "memory check 'valgrind $VALGRIND_OPTIONS ./$OUTPUT_FILE < $test_file'"
valgrind $VALGRIND_OPTIONS ./$OUTPUT_FILE < $test_file

exit 0
