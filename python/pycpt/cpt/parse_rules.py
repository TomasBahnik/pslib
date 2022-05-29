import json
from collections import namedtuple
from datetime import timedelta, datetime
from typing import NamedTuple, Pattern, Callable, Tuple, List

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
        self.rule_result: List[str] = []
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


class Rule(NamedTuple):
    regexp: Pattern
    set: Callable[[ParseResults], None]
    # groups available from regexp pattern
    groups: Tuple[int, ...]
    apply_sub_rules: bool = False
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


conditional_rules = [
    # duration,think time,wasted time goes first
    Rule(END_TRX_PASSED_THINK_TIME, set_transaction_times, (1, 2, 3)),
    # duration,wasted time
    Rule(END_TRX_PASSED, set_transaction_times, (1, 2))
]
all_rules = [
    Rule(SCRIPT_STARTED_RE, set_script_start_time, (1,)),
    Rule(START_ITER, set_iteration_start, (1,)),
    Rule(START_TRX, set_transaction_start, (1,)),
    # with status Pass
    Rule(END_TRX, set_transaction_end, (1, 2), apply_sub_rules=True, sub_rules=conditional_rules),
    Rule(OPERATION_NAME_START_RE, set_gql_request, (1,))
]
