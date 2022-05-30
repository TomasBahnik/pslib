""" Frontend test logs http communication. Parsing that log provides GQL calls and timing for further analyses"""
import json
import os
from pathlib import Path
from typing import List, Tuple, Any

from cpt.common import LR_VUGEN_SCRIPT
from cpt.graphql import OPERATION_NAME
from cpt.parse_rules import Rule, ParseResults, STATUS_PASS
from cpt.templates import fe_transaction_html_template


class LineProcessor:
    """ How to extract (apply rules to) data for particular line in th log file"""

    def __init__(self, rules: List[Rule]):
        self.rules = rules

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
        if rule and len(rule.sub_rules) > 0:
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
                    rule.set(self.pr)
                self.pr.previous_line = stripped

    def print_fe_transactions(self):
        for t in self.pr.ended_fe_transaction:
            print(f'{t.iteration}: {t.trx_name},{t.status},{t.trx_time},{t.end_time},{t.error}')

    def print_gqls(self):
        print(f'{len(self.pr.fet_iter_gql)} gqls')
        for t in self.pr.fet_iter_gql:
            print(f'{t.iteration}: {t.trx_name},{t.gql[OPERATION_NAME]}')

    def save_fe_transactions(self):
        """ Save fe trx as json and html to output dir"""
        fe_trx_dict = [x.__dict__ for x in self.pr.ended_fe_transaction]
        file_prefix = LR_VUGEN_SCRIPT if LR_VUGEN_SCRIPT else 'fe'
        summary_file_name = Path(self.output_dir, f"{file_prefix}_summary")
        with open("{}.json".format(summary_file_name), "w") as json_file:
            json.dump(fe_trx_dict, json_file, indent=4, sort_keys=True)
        html = fe_transaction_html_template().render(trxs=fe_trx_dict)
        with open("{}.html".format(summary_file_name), "w") as html_file:
            html_file.write(html)

    def fe_transaction_elk(self):
        """Prepares and sends ELK events for fe transaction
            number of GQLs inside fe transaction - counts also unassigned GQLs
            build info from GQL API
            most of the fields is copied from self.pr.fe_gql
        """
        self.pr.set_gql_counts()
        self.pr.set_fe_elk_events()
        self.save_elk_events()
        # cpt.elk_events.post_elk_event
        # cpt.parse_trx.post_elk_events
        # post_elk_events - respect property ELK_SENT_EVENTS=true/false
        pass

    def save_elk_events(self):
        script_name = os.getenv('LR_VUGEN_SCRIPT')
        script_name = script_name if script_name else ''
        file_name = Path(self.output_dir, f"{script_name}_feElkEvents.json")
        with open(file_name, "w") as json_file:
            json.dump(self.pr.fe_elk_events, json_file, indent=4, sort_keys=True)

    def save_gqls(self):
        # queries = common.parse_graphql(args.log_file)
        # tests = generate_test_data(queries) = solves identical GQLs, MD5 hash
        # save_tests(tests)  = saves GQls and index json to output dir
        # there is no post elk for GQLs - done by Java code
        # cpt.parse_gqls.generate_test_data
        # cpt.parse_gqls.save_tests
        pass


