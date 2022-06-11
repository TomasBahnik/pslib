#!/bin/bash
export set PYTHONPATH=..

test_compare() {
    python compare_measurements_test.py
}

test_parse_log() {
    python parse_logs_test.py
}

test_kustomize() {
    python kustomize_test.py
}

test_config() {
    python test_config.py
}

echo "test_parse_log"
test_parse_log
echo ""

echo "test_config"
test_config
echo ""

echo "test_compare"
test_compare
echo ""

echo "test_kustomize"
#test_kustomize
echo ""


exit 0
