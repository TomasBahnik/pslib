#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TIMING_FORMAT='+%s.%N'
function timing() {
  printf "%s : %s sec\n" "$1" "$(date $TIMING_FORMAT)"
}

HW=05
TEST_FILES=(pub*.in)
OUTPUT_FILE="b3b36prg-hw$HW"
COMPILE_FILES="../../main.c"
message "remove file '$OUTPUT_FILE'"
rm -f $OUTPUT_FILE
message "compiling with 'clang -pedantic -Wall -Werror -std=c99 -O3 -lm $COMPILE_FILES -o $OUTPUT_FILE'"
clang -pedantic -Wall -Werror -std=c99 -O3 -lm $COMPILE_FILES -o $OUTPUT_FILE
num_of_tests=${#TEST_FILES[@]}
message "running $num_of_tests tests"

FORMAT="%-10s %-5s %s\n\n"
FORMAT_OUT="%-10s %-5s\n"

printf "%s\n" "-------------------------------"
# shellcheck disable=SC2059
printf "$FORMAT" "exit_code" "status" "std error"
printf "%s\n" "-------------------------------"

timing "Test start"
million=1000000
start_time="$(date '+%N')"
start_time_ms=$((start_time / million))
for test_input in "${TEST_FILES[@]}"; do
  test_output_file=${test_input//in/out}
  test_output=$(cat "$test_output_file")
  test_error=${test_input//in/err}
  test_err_content=$(cat "$test_error")
  # call the executable
  error="$(./$OUTPUT_FILE <"$test_input" 2>&1 >/dev/null)"
  exit_code=$?
  if ((exit_code > 0)); then
    echo "exit code = $exit_code"
    if [[ "$error" == "$test_err_content" ]]; then
      res="PASS"
    else
      echo "test file  = $test_input"
      echo ""
      echo "$error"
      echo "expected error"
      echo "$test_err_content"
      res="FAIL"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT" "$exit_code" "$res" "$error"
  else
#    output="$(./$OUTPUT_FILE <"$test_input")"
    echo "test file  = $test_input"
    output="$(./$OUTPUT_FILE <"$test_input")"
    hex_output=$(xxd -pu <<< "$output")
    output_hex=$(echo "$hex_output" | xxd -r -p)
    hex_test_output=$(xxd -pu <<< "$test_output")
#    test_output_hex=$(echo "$hex_test_output" | xxd -r -p)
    if [[ "$output" == "$test_output" ]]; then
      res="PASS"
    else
      res="FAIL"
      printf "hex:%s\n%s\n" "$hex_output" "$output_hex"
      printf "exp_hex:%s\n%s\n" "$hex_test_output" "$test_output"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT_OUT" "$exit_code" "$res"
  fi
done
end_time="$(date '+%N')"
end_time_ms=$((end_time / million))
#elapsed=$((end_time - start_time))
elapsed_ms=$((end_time_ms - start_time_ms))
if ((elapsed_ms < 0)); then
  elapsed_ms=$((1000 + elapsed_ms))
fi
time_per_test=$((elapsed_ms / num_of_tests))
message "Elapsed time = $elapsed_ms ms, time per test = $time_per_test ms"
timing "Test end"
exit 0
