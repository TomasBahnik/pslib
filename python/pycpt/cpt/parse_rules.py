from collections import namedtuple
from datetime import timedelta
from typing import NamedTuple, Pattern, Callable, Any, Tuple, List

from cpt.common import FeTransaction, FeTransaction2Gql, LOG_TIMESTAMP_RE

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
