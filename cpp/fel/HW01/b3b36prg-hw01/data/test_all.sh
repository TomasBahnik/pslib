#!/bin/bash
LOGGER_TIMEFORMAT='+%Y-%m-%dT%H:%M:%S%z'
function message() {
  printf "%s : %s\n" "$(date $LOGGER_TIMEFORMAT)" "$1"
}

TEST_FILES=(pub*.in)
message "compiling with 'clang -pedantic -Wall -Werror -std=c99 ../main.c -o main'"
clang -pedantic -Wall -Werror -std=c99 ../main.c -o main
message "running ${#TEST_FILES[@]} tests"

FORMAT="%-15s %-10s %s\n"
FORMAT_OUT="%-15s %-10s \n\n%s\n\n"

printf "%s\n" "------------------------------"
# shellcheck disable=SC2059
printf "$FORMAT" "test_data" "exit_code" "error"
printf "%s\n" "------------------------------"

for test_file in "${TEST_FILES[@]}"; do
  test_data=$(<"./$test_file")
  error="$(./main <"$test_file" 2>&1 >/dev/null)"
  exit_code=$?
  if ((exit_code > 0)); then
    # shellcheck disable=SC2059
    printf "$FORMAT" "[$test_data]" "$exit_code" "$error"
  else
    output="$(./main <"$test_file")"
    # shellcheck disable=SC2059
    printf "$FORMAT_OUT" "[$test_data]" "$exit_code" "$output"
  fi
done
