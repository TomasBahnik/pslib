import json
from collections import namedtuple
from datetime import timedelta, datetime
from typing import NamedTuple, Pattern, Callable, Any, Tuple, List

from cpt.common import FeTransaction, FeTransaction2Gql, LOG_TIMESTAMP_RE, SCRIPT_STARTED_RE, START_ITER, START_TRX, \
    END_TRX, END_TRX_PASSED_THINK_TIME, END_TRX_PASSED, OPERATION_NAME_START_RE

STATUS_FAIL = 'Fail'
STATUS_PASS = 'Pass'
TransactionTimes = namedtuple('TransactionTimes', 'duration, think, wasted')


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
        self.re_groups_values: List[str] = []
        self.rule_result: Any
        self.fe_gql: List[FeTransaction2Gql] = []

    def process_gql(self, rule_result: dict):
        gql = rule_result
        # TODO fix the logic of assigned trx
        last_opened_fe_trx = self.opened_transaction.pop() if len(self.opened_transaction) > 0 else ''
        trx_gql = FeTransaction2Gql(last_opened_fe_trx, gql, self.current_iteration)
        self.fe_gql.append(trx_gql)

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
            t_times: TransactionTimes = rule_result[2]
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


class Rule(NamedTuple):
    regexp: Pattern
    get: Callable
    # works on LogFile instance rule.set(self, rule_result)
    set: Callable[[ParseResults, Any], None]
    # groups available from regexp pattern
    groups: Tuple[int, ...]


def script_start_time(lp: ParseResults) -> datetime:
    return datetime.strptime(lp.re_groups_values[0], "%Y-%m-%d %H:%M:%S")


def set_script_start_time(x: ParseResults, y): x.script_start_time = y


def iteration_start(lp: ParseResults) -> int:
    return int(lp.re_groups_values[0])


def set_iteration_start(x: ParseResults, y): x.current_iteration = y


def transaction_start(lp: ParseResults) -> str:
    return str(lp.re_groups_values[0])


def set_transaction_start(x: ParseResults, y):
    x.current_transaction = y
    x.opened_transaction.append(y)


def transaction_end(lp: ParseResults) -> Tuple[List[str], bool]:
    # rules for END_TRX_PASSED and END_TRX_PASSED_THINK_TIME are conditioned by passed END_TRX
    conditioned = True
    return lp.re_groups_values, conditioned


def set_transaction_end(x: ParseResults, y): x.process_end_transaction(y)


def gql_request(lp: ParseResults) -> dict:
    pass
    # stripped = lp.line.replace('\\\\', '\\')
    # # when created by cmd line version
    # if "\t" in stripped:
    #     tab = stripped.index("\t")
    #     stripped = stripped[0:tab]
    # gql = json.loads(stripped)
    # return gql


def set_gql_request(x: ParseResults, y):
    stripped = x.line.replace('\\\\', '\\')
    # when created by cmd line version
    if "\t" in stripped:
        tab = stripped.index("\t")
        stripped = stripped[0:tab]
    gql = json.loads(stripped)
    x.process_gql(gql)


def transaction_times(lp: ParseResults):
    ret = [float(x) for x in lp.re_groups_values]
    if len(ret) == 2:
        # think time = 0
        return TransactionTimes(ret[0], 0, ret[1])
    if len(ret) == 3:
        return TransactionTimes(ret[0], ret[1], ret[2])


def set_transaction_times(x: ParseResults, y):
    # no set for transaction_times
    return None


all_rules = [
    Rule(SCRIPT_STARTED_RE, script_start_time, set_script_start_time, (1,)),
    Rule(START_ITER, iteration_start, set_iteration_start, (1,)),
    Rule(START_TRX, transaction_start, set_transaction_start, (1,)),
    # with status Pass
    Rule(END_TRX, transaction_end, set_transaction_end, (1, 2)),
    Rule(OPERATION_NAME_START_RE, gql_request, set_gql_request, (1,))
]
conditional_rules = [
    # duration,think time,wasted time goes first
    Rule(END_TRX_PASSED_THINK_TIME, transaction_times, set_transaction_times, (1, 2, 3)),
    # duration,wasted time
    Rule(END_TRX_PASSED, transaction_times, set_transaction_times, (1, 2))
]
