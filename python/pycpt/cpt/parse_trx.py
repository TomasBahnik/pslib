import argparse
import json
import os

import requests
from jinja2 import Template

from cpt.common import parse_graphql, fe_trans_gql_count, ELK_BASE_URL, parse_transactions
from elk_events import ELKEvent

# relative to CPT root
UI_TRANSACTION = "ui_transaction"
TEST_RESULTS = "modules/api-tests/test-results/"
# Notify: Transaction "One_Basic_Login" ended with a "Pass" status (Duration: 8.5820 Wasted Time: 3.3030)
# Notify: Transaction "One_Basic_Sources" started.
parser = argparse.ArgumentParser(description='Read GQLs from FE test')
parser.add_argument(
    "--log_file",
    required=True,
    help="true client log file"
)

parser.add_argument(
    "--output_dir",
    default=TEST_RESULTS,
    help="directory for test results"
)

args = parser.parse_args()

if not os.path.exists(args.output_dir):
    print("Create dir {}".format(os.path.abspath(args.output_dir)))
    os.makedirs(args.output_dir)

SQL_SERVICE_TYPE = os.getenv('SQL_SERVICE_TYPE')
TEST_ENV = os.getenv('TEST_ENV')
LOG_DIR_TIMESTAMP = os.getenv('LOG_DIR_TIMESTAMP')  # denotes current logging directory
LR_VUGEN_SCRIPT = os.getenv('LR_VUGEN_SCRIPT')
GIT_BRANCH = os.getenv('GIT_BRANCH')
GIT_COMMIT = os.getenv('GIT_COMMIT')
APP_GQL_URL = os.getenv('APP_GQL_URL')

print("OS env vars TEST_ENV={}, LOG_DIR_TIMESTAMP={}, LR_VUGEN_SCRIPT={}, "
      "GIT_BRANCH={}, GIT_COMMIT={}, SQL_SERVICE_TYPE={}, APP_GQL_URL={}, cpt_common.ELK_BASE_URL={}"
      .format(TEST_ENV, LOG_DIR_TIMESTAMP, LR_VUGEN_SCRIPT, GIT_BRANCH, GIT_COMMIT,
              SQL_SERVICE_TYPE, APP_GQL_URL, ELK_BASE_URL))


def html_template(test_env='test_env', log_dir='log_dir', script_name='script_name') -> Template:
    return Template('''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    </head>
    <body>
    <h2>FE transactions</h2>
    <table border="1">
        <tr><th>Iteration</th><th>Name</th><th>Trx time</th><th>Wasted time</th><th>End time</th></tr>
        {% for trx in trxs %}
        <tr><td>{{ trx['iteration'] }}</td> <td>{{ trx['trx_name'] }}</td> <td>{{ trx['trx_time'] }}</td> <td>{{ trx['wasted_time'] }}</td><td>{{ trx['end_time'] }}</td></tr>
        {% endfor %}
    </table>
    <p>'Trx time' = duration - wasted_time. Wasted time is the time spent by the tool to capture and process data during test run</p>
    <a href=../../../log/''' + test_env + '/' + log_dir
                    + '/' + script_name + '>Log dir of the FE test</a>' +
                    '''
    </body>
    </html> 
    ''')


BUILD_INFO_GQL = {
    "query": "query getBuildInfo {\n  _buildInfo {\n    branch\n    buildHost\n    buildUserName\n    buildVersion\n  "
             "  commitId\n    commitIdAbbrev\n    commitTime\n    commitUserName\n    totalCommitCount\n  }\n}\n",
    "operationName": "getBuildInfo"}


def build_info(be_url):
    r = requests.post(be_url, auth=('admin', 'admin'), verify=False, json=BUILD_INFO_GQL)
    if r.status_code != 200:
        return None
    build_info_data = r.json()['data']['_buildInfo']
    print("Build info {}", build_info_data)
    return build_info_data


class FeTransactionTestResultEvent:
    # only OS envs in constructor
    # field names according to com.ataccama.one.performance.model.TestResultEvent
    def __init__(self, testEnv, cptBranch, cptHeadCommit):
        self.testEnv = testEnv
        self.cptBranch = cptBranch
        self.cptHeadCommit = cptHeadCommit
        self.scriptName = None
        self.trxName = None
        self.result = None
        self.duration = -1
        self.testError = None
        # from build info POST to https://backend-toba-perf.build.atc/graphql
        self.appBranch = None
        self.appHeadCommit = None
        self.sqlServiceType = None
        self.gqlCount = -1
        self.iteration = 0


def prepare_test_results_events(transactions, log_file):
    events = []
    elk_events = []
    trx_gqls = parse_graphql(log_file)
    fe_trx_gql_counts = fe_trans_gql_count(trx_gqls)
    bi = build_info(APP_GQL_URL)
    if bi is None:
        app_branch = None
        app_head_commit = None
    else:
        app_branch = bi['branch']
        app_head_commit = bi['commitId']
    for trx in transactions:
        event = FeTransactionTestResultEvent(TEST_ENV, GIT_BRANCH, GIT_COMMIT)
        event.duration = trx['trx_time']
        event.trxName = trx['trx_name']
        event.scriptName = LR_VUGEN_SCRIPT
        event.iteration = trx['iteration']
        event.result = str(trx['status']).lower()
        event.testError = trx['error']
        event.appBranch = app_branch
        event.appHeadCommit = app_head_commit
        event.sqlServiceType = SQL_SERVICE_TYPE
        filtered_fe_trx = [fe_trx for fe_trx in fe_trx_gql_counts if
                           fe_trx.trx_name == event.trxName and fe_trx.iteration == event.iteration]
        event.gqlCount = filtered_fe_trx[0].gql_count if len(filtered_fe_trx) == 1 else None
        events.append(event.__dict__)
        elk_event = ELKEvent('fe-test-results', event.__dict__, trx['end_time'])
        elk_events.append(elk_event.__dict__)
    print("test_results_events size : {}".format(len(events)))
    print("elk test_results_events size : {}".format(len(elk_events)))
    return elk_events


def save_tests(trxs):
    file_prefix = (LR_VUGEN_SCRIPT if LR_VUGEN_SCRIPT is not None else 'fe')
    output_dir = check_output_dir()
    summary_base_file_name = "{}{}_summary".format(output_dir, file_prefix)
    print("summary_base_file_name : {}".format(summary_base_file_name))
    with open("{}.json".format(summary_base_file_name), "w") as json_file:
        json.dump(trxs, json_file, indent=4, sort_keys=True)
    html = html_template().render(trxs=trxs)
    with open("{}.html".format(summary_base_file_name), "w") as html_file:
        html_file.write(html)


def check_output_dir():
    if str(args.output_dir).endswith("/"):
        output_dir = args.output_dir
    else:
        output_dir = args.output_dir + "/"
    return output_dir


def save_elk_events(events):
    output_dir = check_output_dir()
    file_name = output_dir + LR_VUGEN_SCRIPT + '_feElkEvents.json'
    with open(file_name, "w") as json_file:
        json.dump(events, json_file, indent=4, sort_keys=True)


def post_elk_events(elk_events):
    for elk_event in elk_events:
        elk_url = ELK_BASE_URL + elk_event['eventType']
        r = requests.post(elk_url, verify=False, json=elk_event, timeout=10)  # in seconds
        print("POST to {} status code {}", elk_url, r.status_code)


if __name__ == '__main__':
    print("Using log file '{}' and writing output to {}".format(args.log_file,
                                                                os.path.abspath(args.output_dir)))
    trxs = parse_transactions(args.log_file)
    if len(trxs) > 0:
        save_tests(trxs)
        elk_events = prepare_test_results_events(trxs, args.log_file)
        save_elk_events(elk_events)
        if LR_VUGEN_SCRIPT.endswith("Helper"):
            print("'{}' is helper script. Do not POST events to ELK".format(LR_VUGEN_SCRIPT))
        else:
            print("Script '{}' POSTs events to ELK".format(LR_VUGEN_SCRIPT))
            post_elk_events(elk_events)
    else:
        print("There are no fe transactions")
