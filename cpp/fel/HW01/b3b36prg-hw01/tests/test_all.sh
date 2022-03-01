#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TEST_FILES=(*.txt)
message "compiling clang ../main.c -o main"
clang ../main.c -o main
message "running ${#TEST_FILES[@]} tests"

FORMAT="%-15s %-10s %s\n"

printf "%s\n"    "------------------------------"
# shellcheck disable=SC2059
printf "$FORMAT" "test_data" "exit_code" "error"
printf "%s\n"    "------------------------------"

for test_file in "${TEST_FILES[@]}"; do
  test_data=$(<"./$test_file")
  error="$(./main <"$test_file" 2>&1 > /dev/null)"
  exit_code=$?
  # shellcheck disable=SC2059
  printf "$FORMAT" "[$test_data]" "$exit_code" "$error"
done
