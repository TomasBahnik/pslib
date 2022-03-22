#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TIMING_FORMAT='+%s.%N'
function timing() {
  printf "%s : %s sec\n" "$1" "$(date $TIMING_FORMAT)"
}

HW=03
TEST_FILES=(pub*.in)
OUTPUT_FILE="b3b36prg-hw$HW"
COMPILE_FILES="../main.c"
message "remove file '$OUTPUT_FILE'"
rm -f $OUTPUT_FILE
message "compiling with 'clang -pedantic -Wall -Werror -std=c99 -O3 -lm $COMPILE_FILES -o $OUTPUT_FILE'"
clang -pedantic -Wall -Werror -std=c99 -O3 -lm $COMPILE_FILES -o $OUTPUT_FILE
num_of_tests=${#TEST_FILES[@]}
message "running $num_of_tests tests"

FORMAT="%-10s %-5s %s\n"
FORMAT_OUT="%-10s %-5s\n"

printf "%s\n" "-------------------------------"
# shellcheck disable=SC2059
printf "$FORMAT" "exit_code" "status" "std error"
printf "%s\n" "-------------------------------"

timing "Test start"
start_time="$(date '+%N')"
for test_input in "${TEST_FILES[@]}"; do
  test_output_file=${test_input//in/out}
  test_output=$(cat "$test_output_file")
  test_error=${test_input//in/err}
  test_err_content=$(cat "$test_error")
  #  test_data=$(<"./$test_input")
  error="$(./$OUTPUT_FILE <"$test_input" 2>&1 >/dev/null)"
  exit_code=$?
  if ((exit_code > 0)); then
    if [[ "$error" == "$test_err_content" ]]; then
      res="PASS"
    else
      res="FAIL"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT" "$exit_code" "$res" "$error"
  else
    output="$(./$OUTPUT_FILE <"$test_input")"
    if [[ "$output" == "$test_output" ]]; then
      res="PASS"
    else
      res="FAIL"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT_OUT" "$exit_code" "$res"
  fi
done
end_time="$(date '+%N')"
elapsed=$((end_time - start_time))
elapsed_ms=$((elapsed / 1000000))
if ((elapsed_ms < 0)); then
  elapsed_ms=$((1000 + elapsed_ms))
fi
time_per_test=$((elapsed_ms / num_of_tests))
message "Elapsed time = $elapsed_ms ms, time per test = $time_per_test ms"
timing "Test end"
exit 0