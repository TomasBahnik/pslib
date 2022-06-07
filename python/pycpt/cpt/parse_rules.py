import json
import os
import socket
from collections import namedtuple
from datetime import timedelta, datetime
from typing import NamedTuple, Pattern, Callable, Tuple, List

import requests

from cpt.common import FeTransaction, FeTransaction2Gql, LOG_TIMESTAMP_RE, SCRIPT_STARTED_RE, START_ITER, START_TRX, \
    END_TRX, END_TRX_PASSED_THINK_TIME, END_TRX_PASSED, OPERATION_NAME_START_RE, FeTransactionGqlCount

STATUS_FAIL = 'Fail'
STATUS_PASS = 'Pass'
TransactionTimes = namedtuple('TransactionTimes', 'duration, think, wasted')

MMM_BUILD_INFO_GQL = {
    "query": "query getBuildInfo {\n  _buildInfo {\n    branch\n    buildHost\n    buildUserName\n    buildVersion\n  "
             "  commitId\n    commitIdAbbrev\n    commitTime\n    commitUserName\n    totalCommitCount\n  }\n}\n",
    "operationName": "getBuildInfo"}


def build_info(be_url):
    if be_url is None:
        return None
    r = requests.post(be_url, auth=('admin', 'admin'), verify=False, json=MMM_BUILD_INFO_GQL)
    if r.status_code != 200:
        return None
    ret = r.json()['data']['_buildInfo']
    if ret:
        return ret
    else:
        return None


class ELKEvent:
    def __init__(self, event_type: str, event: dict, timestamp):
        self.eventType = event_type
        self.event = event
        self.timestamp = timestamp
        self.eventBuildInfo = None
        self.eventSourceHost = None


class FeTransactionTestResultEvent:
    # only OS envs in constructor
    # field names according to com.ataccama.one.performance.model.TestResultEvent
    def __init__(self, test_env: str = 'test_env', cpt_branch: str = 'cpt_branch',
                 cpt_head_commit: str = 'cpt_head_commit'):
        self.testEnv = test_env
        self.cptBranch = cpt_branch
        self.cptHeadCommit = cpt_head_commit
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


class ParseResults:
    def __init__(self):
        self.script_start_time = None
        self.current_iteration: int = 0
        self.ended_fe_transaction: List[FeTransaction] = []
        self.current_transaction: str = ''
        self.opened_transaction: List[str] = []
        # remember previous line with relative timestamp for error and end time
        self.previous_line: str = ''
        self.line: str = ''
        self.rule_result: List[str] = []
        # table [fe_trans, iteration, gql] created during parsing
        self.fet_iter_gql: List[FeTransaction2Gql] = []
        # table [fe_trans, iteration, n_gqls]
        self.fet_iter_n_gqls: List[FeTransactionGqlCount] = []
        self.fe_elk_events: List[dict] = []
        self.build_info = build_info(os.getenv('APP_GQL_URL'))

    def process_gql(self, rule_result: dict):
        gql = rule_result
        last_opened_fe_trx = self.opened_transaction[-1] if len(self.opened_transaction) > 0 else None
        trx_gql = FeTransaction2Gql(last_opened_fe_trx, gql, self.current_iteration)
        self.fet_iter_gql.append(trx_gql)

    def fe_trx_end_time(self) -> str:
        """ ISO time for transaction end"""
        match = LOG_TIMESTAMP_RE.match(self.previous_line)
        if match:
            t = int(match.group(1))
            end_time = self.script_start_time + timedelta(milliseconds=t)
            return end_time.isoformat()
        return ''

    def process_end_transaction(self, rule_result):
        # event_result = name , status, times (for Passed trx)
        name = rule_result[0]
        status = rule_result[1]
        if status == STATUS_PASS:
            t_times: TransactionTimes = transaction_times(self)
            # trx_time is calculated during initialization
            fet = FeTransaction(name=name, status=status,
                                duration=t_times.duration,
                                wasted_time=t_times.wasted,
                                think_time=t_times.think,
                                end_time=self.fe_trx_end_time(),
                                iteration=self.current_iteration)
            self.ended_fe_transaction.append(fet)
        if status == STATUS_FAIL:
            fet = FeTransaction(name=name, status=status,
                                end_time=self.fe_trx_end_time(),
                                error=self.previous_line,
                                iteration=self.current_iteration)
            self.ended_fe_transaction.append(fet)
        self.update_opened_fe_transaction(name)

    def update_opened_fe_transaction(self, ended_trans: str):
        try:
            self.opened_transaction.remove(ended_trans)
        except ValueError as e:
            pass

    def get_gql_count(self, fet_name, iteration):
        ret = [x.gql_count for x in self.fet_iter_n_gqls
               if x.trx_name == fet_name and x.iteration == iteration]
        return int(ret[0]) if len(ret) == 1 else None

    def set_gql_counts(self):
        # creates set
        fe_transactions = {trx_gql.trx_name for trx_gql in self.fet_iter_gql}
        fe_iterations = {trx_gql.iteration for trx_gql in self.fet_iter_gql}
        for i in sorted(fe_iterations):
            for fe_trx in fe_transactions:
                trx_gql_count = [x for x in self.fet_iter_gql
                                 if (x.trx_name == fe_trx and int(x.iteration) == int(i))]
                gql_count = len(trx_gql_count)
                item = FeTransactionGqlCount(fe_trx, gql_count, i)
                self.fet_iter_n_gqls.append(item)

    def map_to_elk(self, source: FeTransaction) -> FeTransactionTestResultEvent:
        ret = FeTransactionTestResultEvent(os.getenv('TEST_ENV'),
                                           os.getenv('GIT_BRANCH'),
                                           os.getenv('GIT_COMMIT'))
        ret.scriptName = os.getenv('LR_VUGEN_SCRIPT')
        ret.appBranch = self.build_info['branch'] if self.build_info else None
        ret.appHeadCommit = self.build_info['commitId'] if self.build_info else None
        ret.sqlServiceType = os.getenv('SQL_SERVICE_TYPE')
        ret.iteration = source.iteration
        ret.duration = source.duration
        ret.trxName = source.trx_name
        ret.result = source.status
        ret.testError = source.error
        ret.gqlCount = self.get_gql_count(source.trx_name, source.iteration)
        return ret

    def set_fe_elk_events(self):
        """ Map self.fe_gql to FeTransactionTestResultEvent"""
        for fet in self.ended_fe_transaction:
            elk = self.map_to_elk(fet)
            elk_event = ELKEvent('fe-test-results', elk.__dict__, fet.end_time)
            # TODO duplicated
            elk_event.eventBuildInfo = self.build_info
            elk_event.eventSourceHost = socket.gethostname()
            self.fe_elk_events.append(elk_event.__dict__)


class Rule(NamedTuple):
    regexp: Pattern
    # groups available from regexp pattern
    groups: Tuple[int, ...] = (1,)
    set: Callable[[ParseResults], None] = lambda x: None
    sub_rules: List = []


def set_script_start_time(x: ParseResults):
    y = x.rule_result
    x.script_start_time = datetime.strptime(y[0], "%Y-%m-%d %H:%M:%S")


def set_iteration_start(x: ParseResults):
    y = x.rule_result
    x.current_iteration = int(y[0])


def set_transaction_start(x: ParseResults):
    y = x.rule_result
    trx = str(y[0])
    x.current_transaction = trx
    x.opened_transaction.append(trx)


def set_transaction_end(x: ParseResults):
    y = x.rule_result
    x.process_end_transaction(y)


def set_gql_request(x: ParseResults):
    stripped = x.line.replace('\\\\', '\\')
    # when created by cmd line version
    if "\t" in stripped:
        tab = stripped.index("\t")
        stripped = stripped[0:tab]
    gql = json.loads(stripped)
    x.process_gql(gql)


def transaction_times(lp: ParseResults):
    ret = [float(x) for x in lp.rule_result[2]]
    if len(ret) == 2:
        # think time = 0
        return TransactionTimes(ret[0], 0, ret[1])
    if len(ret) == 3:
        return TransactionTimes(ret[0], ret[1], ret[2])


def set_transaction_times(x: ParseResults, y):
    # no set for transaction_times
    return None


transaction_end_rules = [
    # duration,think time,wasted time goes first
    Rule(END_TRX_PASSED_THINK_TIME, groups=(1, 2, 3)),
    # duration,wasted time
    Rule(END_TRX_PASSED, groups=(1, 2))
]
request_response_log_rules = [
    Rule(SCRIPT_STARTED_RE, set=set_script_start_time),
    Rule(START_ITER, set=set_iteration_start),
    Rule(START_TRX, set=set_transaction_start),
    # with status Pass
    Rule(END_TRX, groups=(1, 2), set=set_transaction_end, sub_rules=transaction_end_rules),
    Rule(OPERATION_NAME_START_RE, set=set_gql_request)
]
