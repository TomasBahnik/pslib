import argparse
import datetime
import hashlib
import json
import os
import sys
from copy import copy

from cpt import common
from graphql import GQL_ORDER, GQL_LENGTH, GQL_VARIABLES_LENGTH, GQL_HASH_MD5, OPERATION_NAME, GQL_VARIABLES_HASH_MD5

TEST_RUN_KEY = 'testRun'
TEST_RUNS = 2

TEST_TAG = "testTag"
UI_TRANSACTION = "uiTransaction"
VARIABLES = 'variables'
QUERY = 'query'
OPERATION_NAME_ORIG = 'operationName_orig'
QUERY_ORIG = 'query_orig'
COMMON_DATA_GENERATED = "modules/api-tests/resources/common/data/generated/"

parser = argparse.ArgumentParser(description='Read GQLs from FE test')
parser.add_argument(
    "--log_file",
    help="true client log file"
)
parser.add_argument(
    "--output_dir",
    default=COMMON_DATA_GENERATED,
    help="directory for generated data"
)

args = parser.parse_args()

if not os.path.exists(args.output_dir):
    print("Create dir {}".format(os.path.abspath(args.output_dir)))
    os.makedirs(args.output_dir)


def generate_test_data(test_requests):
    tests = []
    gql_counter = {}  # key operationName, value count
    k = 0  # counts identical gqls
    o = 1  # counts operation names
    test_tag = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    if len(test_requests) == 0:
        print("There are no queries, return")
        return tests
    for trx_gql in test_requests:
        gql = trx_gql.gql
        test = {}
        operation_name = gql[OPERATION_NAME]
        variables = gql[VARIABLES]
        query = gql[QUERY]
        test[TEST_TAG] = test_tag + "_" + trx_gql.iteration
        test[UI_TRANSACTION] = trx_gql.trx_name
        test[VARIABLES] = variables
        compact_vars_str = "".join(str(variables).split())
        compact_query_str = "".join(str(query).split())
        test[GQL_VARIABLES_LENGTH] = len(compact_vars_str)
        test[GQL_LENGTH] = len(compact_query_str)
        # add this stable hash for checking
        test[GQL_HASH_MD5] = hashlib.md5(compact_query_str.encode('utf-8')).hexdigest()
        test[GQL_VARIABLES_HASH_MD5] = hashlib.md5(compact_vars_str.encode('utf-8')).hexdigest()
        test[OPERATION_NAME] = operation_name
        test[QUERY] = query
        test[OPERATION_NAME_ORIG] = operation_name
        test[QUERY_ORIG] = query
        print("{}. operation name : {}".format(o, test[OPERATION_NAME]))
        o = o + 1
        same = same_gql(tests, query, operation_name)
        if same is not None:
            print("\t{} : graphqls are the same".format(test[OPERATION_NAME]))
            test[OPERATION_NAME] = same[OPERATION_NAME]
            test[QUERY] = same[QUERY]
            tests.append(test)
            continue
        different = different_gql(tests, query, operation_name)
        if different is not None:
            try:
                gql_count = gql_counter[operation_name]
                print("\t{} : Increasing GQL order to {}".format(operation_name, gql_count + 1))
                gql_counter[operation_name] += 1
            except KeyError as k_e:
                # first appearance of different GQL with the same operation name => label 1
                gql_counter[operation_name] = 1
                print("\t{} : GQL order initialized".format(k_e))

            gql_order = gql_counter[operation_name]
            print("\t{} : GQLs are different. GQL order {}, total order {}".format(test[OPERATION_NAME], gql_order, k))
            test[GQL_ORDER] = gql_order
            test[OPERATION_NAME] = operation_name + str(k)
            query = str(query).replace(operation_name, test[OPERATION_NAME], 1)
            test[QUERY] = query
            k = k + 1
            tests.append(test)
            continue
        tests.append(test)
    return tests


def save_tests(tests):
    if str(args.output_dir).endswith("/"):
        output_dir = args.output_dir
    else:
        output_dir = args.output_dir + "/"
    for test in tests:
        test.pop(QUERY_ORIG)
        test.pop(OPERATION_NAME_ORIG)
        try:
            with open(output_dir + test[OPERATION_NAME] + ".graphql", "w") as gql_file:
                gql_file.write(test.pop(QUERY))  # remove query after storing it to file
        except FileNotFoundError as fnf:  # in case of invalid file name
            print('Removing {}'.format(test[OPERATION_NAME]))
            # remove from index.json
            tests.remove(test)
            print(fnf)
    # tests are without gqls, only variables and operation names
    tests_multiple_runs = []  # run the same GQL multiple time
    for t in tests:
        for r in range(TEST_RUNS):
            tests_multiple_runs.append(copy(t))
            tests_multiple_runs[-1][TEST_RUN_KEY] = r + 1  # 1 based
    with open("%sindex.json" % output_dir, "w") as json_file:
        json.dump(tests_multiple_runs, json_file, indent=4, sort_keys=True)


def same_gql(tests, gql, operation_name):
    for test in tests:
        if str(test[OPERATION_NAME_ORIG]) == operation_name and test[QUERY_ORIG] == gql:
            return test
    return None


def different_gql(tests, gql, operation_name):
    for test in tests:
        if str(test[OPERATION_NAME_ORIG]) == operation_name and test[QUERY_ORIG] != gql:
            return test
    return None


if __name__ == '__main__':
    print("Using log file '{}' and generating data to {}".format(args.log_file,
                                                                 os.path.abspath(args.output_dir)))
    queries = common.parse_graphql(args.log_file)
    tests = generate_test_data(queries)
    save_tests(tests)
    sys.exit(0)
