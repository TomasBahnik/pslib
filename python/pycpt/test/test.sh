#!/bin/bash
export set PYTHONPATH=..

test_compare() {
    python comapare_measurements_test.py
}

test_parse_log() {
    python parse_logs_test.py
}

test_kustomize() {
    python kustomize_test.py
}

echo "test_parse_log"
test_parse_log
echo .


echo "test_compare"
test_compare
echo .

echo "test_kustomize"
test_kustomize
echo .

exit 0
