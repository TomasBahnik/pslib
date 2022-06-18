#!/bin/bash
# ./bin/pycpt/test/test.sh

test_compare() {
    python bin/pycpt/compare_cmd.py --folder-1 bin/pycpt/test/csv/paas_ci --folder-2 bin/pycpt/test/csv/paas_dq
}

test_parse_log() {
    python parse_logs_test.py
}

test_kustomize() {
    python bin/pycpt/redeploy_paas.py --test-env paas_ci --step build
}

test_child_pipeline() {
    python bin/pycpt/child_pipeline.py --test-env paas_ci --step api_tests
}

#echo "test_parse_log"
#test_parse_log
#echo ""

echo "test_compare"
test_compare
echo ""

echo "test_kustomize"
test_kustomize
echo ""

echo "test_child_pipeline"
test_child_pipeline
echo ""

exit 0
