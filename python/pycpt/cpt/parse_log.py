""" Frontend test logs http communication. Parsing that log provides GQL calls and timing for further analyses"""
from pathlib import Path
from typing import List, Tuple, Any

from cpt.graphql import OPERATION_NAME
from cpt.parse_rules import Rule, ParseResults, STATUS_PASS


class LineProcessor:
    """ How to extract (apply rules to) data for particular line in th log file"""

    def __init__(self, rules: List[Rule], cond_rules: List[Rule]):
        self.rules = rules
        self.cond_rules = cond_rules
        self.re_groups_values: List[str] = []
        self.line: str = ''

    @staticmethod
    def process_rules(line: str, rules: List[Rule]) -> Tuple[Any, Any]:
        for rule in rules:
            regexp_match = rule.regexp.match(line)
            if regexp_match:
                rule_result = [regexp_match.group(x) for x in rule.groups]
                return rule, rule_result
            else:
                continue
        return None, None

    def process_line(self, line: str) -> Tuple[Any, Any]:
        rule, rule_result = self.process_rules(line, self.rules)
        # conditional expressed by 2nd value = True
        if rule and rule.apply_sub_rules:
            trx_name, trx_status = rule_result
            if trx_status == STATUS_PASS:
                # event_name is always transaction_times
                _, trx_times = self.process_rules(line, rule.sub_rules)
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
                (rule, rule_result) = self.lp.process_line(stripped)
                if (rule, rule_result) != (None, None):
                    self.pr.line = stripped
                    self.pr.rule_result = rule_result
                    rule.set(self.pr, rule_result)
                self.pr.previous_line = stripped

    def print_fe_transactions(self):
        for t in self.pr.ended_fe_transaction:
            print(f'{t.iteration}: {t.trx_name},{t.status},{t.trx_time},{t.end_time},{t.error}')

    def print_gqls(self):
        print(f'{len(self.pr.fe_gql)} gqls')
        for t in self.pr.fe_gql:
            print(f'{t.iteration}: {t.trx_name},{t.gql[OPERATION_NAME]}')
