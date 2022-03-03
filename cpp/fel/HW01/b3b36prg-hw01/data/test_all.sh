#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TEST_FILES=(pub*.in)
OUTPUT_FILE=b3b36prg-hw01
message "remove file '$OUTPUT_FILE'"
rm -f $OUTPUT_FILE
message "compiling with 'clang -pedantic -Wall -Werror -std=c99 ../main.c -o $OUTPUT_FILE'"
clang -pedantic -Wall -Werror -std=c99 ../main.c -o $OUTPUT_FILE
message "running ${#TEST_FILES[@]} tests"

FORMAT="%-15s %-10s %-5s %s\n"
FORMAT_OUT="%-15s %-10s %-5s \n%s\n \n%s\n\n"

printf "%s\n" "--------------------------------------------------"
# shellcheck disable=SC2059
printf "$FORMAT" "test_data" "exit_code" "status" "std error"
printf "%s\n" "--------------------------------------------------"

for test_input in "${TEST_FILES[@]}"; do
  test_output_file=${test_input//in/out}
  test_output=$(cat "$test_output_file")
  test_error=${test_input//in/err}
  test_err_content=$(cat "$test_error")
  test_data=$(<"./$test_input")
  error="$(./$OUTPUT_FILE <"$test_input" 2>&1 >/dev/null)"
  exit_code=$?
  if ((exit_code > 0)); then
    if [[ "$error" == "$test_err_content" ]]; then
      res="PASS"
    else
      res="FAIL"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT" "[$test_data]" "$exit_code" "$res" "$error"
  else
    output="$(./$OUTPUT_FILE <"$test_input")"
    if [[ "$output" == "$test_output" ]]; then
      res="PASS"
    else
      res="FAIL"
    fi
    # shellcheck disable=SC2059
    printf "$FORMAT_OUT" "[$test_data]" "$exit_code" "$res" "$output" "$test_output"
  fi
done
