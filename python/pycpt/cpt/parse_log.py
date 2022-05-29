""" Frontend test logs http communication. Parsing that log provides GQL calls and timing for further analyses"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Any

from cpt.common import SCRIPT_STARTED_RE, START_ITER, START_TRX, \
    END_TRX, OPERATION_NAME_START_RE, END_TRX_PASSED_THINK_TIME, END_TRX_PASSED
from cpt.graphql import OPERATION_NAME
from cpt.parse_rules import Rule, ParseResults, STATUS_PASS, TransactionTimes


class LineProcessor:
    """ How to extract (apply rules to) data for particular line in th log file"""

    def __init__(self, rules: List[Rule], cond_rules: List[Rule]):
        self.rules = rules
        self.cond_rules = cond_rules
        self.re_groups_values: List[str] = []
        self.line: str = ''

    def process_rules(self, line: str, rules: List[Rule]) -> Tuple[Any, Any]:
        for rule in rules:
            regexp_match = rule.regexp.match(line)
            if regexp_match:
                self.re_groups_values = [regexp_match.group(x) for x in rule.groups]
                get_val = rule.get(self)
                # only the first one regexp applies for given line
                return rule, get_val
            else:
                continue
        return None, None

    def process_line(self, line: str) -> Tuple[Any, Any]:
        rule, rule_result = self.process_rules(line, self.rules)
        # conditional expressed by 2nd value = True
        if rule and isinstance(rule_result, Tuple) and rule_result[1]:
            trx_name, trx_status = rule_result[0]
            if trx_status == STATUS_PASS:
                # event_name is always transaction_times
                _, trx_times = self.process_rules(line, self.cond_rules)
                return rule, [trx_name, trx_status, trx_times]
        return rule, rule_result


class LogFile:
    """ keep content of log file in structures """

    def __init__(self, log_file: Path, output_dir: Path, pr: ParseResults, lp: LineProcessor):
        self.log_file = log_file
        self.output_dir = output_dir
        self.pr = pr
        self.lp = lp

    def parse_all(self):
        with open(self.log_file, encoding='windows-1252') as input_file:
            for line in input_file.readlines():
                stripped = line.strip()
                self.lp.line = stripped
                (rule, rule_result) = self.lp.process_line(stripped)
                if (rule, rule_result) != (None, None):
                    rule.set(self.pr, rule_result)
                self.pr.previous_line = stripped

    def print_fe_transactions(self):
        for t in self.pr.ended_fe_transaction:
            print(f'{t.iteration}: {t.trx_name},{t.status},{t.trx_time},{t.end_time},{t.error}')

    def print_gqls(self):
        print(f'{len(self.pr.fe_gql)} gqls')
        for t in self.pr.fe_gql:
            print(f'{t.iteration}: {t.trx_name},{t.gql[OPERATION_NAME]}')


# rule get/set functions


def script_start_time(lp: LineProcessor) -> datetime:
    return datetime.strptime(lp.re_groups_values[0], "%Y-%m-%d %H:%M:%S")


def set_script_start_time(x: ParseResults, y): x.script_start_time = y


def iteration_start(lp: LineProcessor) -> int:
    return int(lp.re_groups_values[0])


def set_iteration_start(x: ParseResults, y): x.current_iteration = y


def transaction_start(lp: LineProcessor) -> str:
    return str(lp.re_groups_values[0])


def set_transaction_start(x: ParseResults, y):
    x.current_transaction = y
    x.opened_transaction.append(y)


def transaction_end(lp: LineProcessor) -> Tuple[List[str], bool]:
    # rules for END_TRX_PASSED and END_TRX_PASSED_THINK_TIME are conditioned by passed END_TRX
    conditioned = True
    return lp.re_groups_values, conditioned


def set_transaction_end(x: ParseResults, y): x.process_end_transaction(y)


def gql_request(lp: LineProcessor) -> dict:
    stripped = lp.line.replace('\\\\', '\\')
    # when created by cmd line version
    if "\t" in stripped:
        tab = stripped.index("\t")
        stripped = stripped[0:tab]
    gql = json.loads(stripped)
    return gql


def set_gql_request(x: ParseResults, y): x.process_gql(y)


def transaction_times(lp: LineProcessor):
    ret = [float(x) for x in lp.re_groups_values]
    if len(ret) == 2:
        # think time = 0
        return TransactionTimes(ret[0], 0, ret[1])
    if len(ret) == 3:
        return TransactionTimes(ret[0], ret[1], ret[2])


def set_transaction_times(x: ParseResults, y):
    # no set for transaction_times
    return None


basic_rules = [
    Rule(SCRIPT_STARTED_RE, script_start_time, set_script_start_time, (1,)),
    Rule(START_ITER, iteration_start, set_iteration_start, (1,)),
    Rule(START_TRX, transaction_start, set_transaction_start, (1,)),
    # with status Pass
    Rule(END_TRX, transaction_end, set_transaction_end, (1, 2)),
]

all_rules = basic_rules + [Rule(OPERATION_NAME_START_RE, gql_request, set_gql_request, (1,))]

conditional_rules = [
    # duration,think time,wasted time goes first
    Rule(END_TRX_PASSED_THINK_TIME, transaction_times, set_transaction_times, (1, 2, 3)),
    # duration,wasted time
    Rule(END_TRX_PASSED, transaction_times, set_transaction_times, (1, 2))
]
