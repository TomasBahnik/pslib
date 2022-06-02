""" Frontend test logs http communication. Parsing that log provides GQL calls and timing for further analyses"""
import datetime
import hashlib
import json
import os
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Any

from cpt.common import error_print
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


def md5_str(input_str: str) -> str:
    joined_str = ''.join(str(input_str).split())
    return hashlib.md5(joined_str.encode('utf-8')).hexdigest()


def joined_length(input_str: str) -> int:
    joined_str = ''.join(str(input_str).split())
    return len(joined_str)


@dataclass
class GqlTest:
    testTag: str
    uiTransaction: str
    operationName: str
    variables: str
    gqlQuery: str
    testRun: int = 0
    gqlQueryPath: str = None
    gqlHashMD5: str = None
    variablesHashMD5: str = None
    gqlLength: int = 0
    variablesLength: int = 0

    def __post_init__(self):
        self.gqlLength: int = joined_length(self.gqlQuery)
        self.variablesLength: int = joined_length(self.variables)
        self.gqlHashMD5: str = md5_str(self.gqlQuery)
        self.variablesHashMD5: str = md5_str(self.variables)
        self.gqlQueryPath: str = f'{self.gqlHashMD5}/{self.operationName}'


class LogFile:
    """ keep content of log file in structures """

    def __init__(self, log_file: Path, output_dir: Path,
                 pr: ParseResults,
                 lp: LineProcessor,
                 test_runs: int = 4,
                 vugen_script: str = 'fe'):
        self.log_file = log_file
        self.output_dir = output_dir
        self.pr = pr
        self.lp = lp
        self.test_runs = test_runs
        self.vugen_script = vugen_script

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
        summary_file_name = Path(self.output_dir, f"{self.vugen_script}_summary")
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
        file_name = Path(self.output_dir, f"{self.vugen_script}_feElkEvents.json")
        with open(file_name, "w") as json_file:
            json.dump(self.pr.fe_elk_events, json_file, indent=4, sort_keys=True)

    def save_gqls(self):
        test_tag = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        gql_tests: List[GqlTest] = []
        for g in self.pr.fet_iter_gql:
            t_t = test_tag + "_" + str(g.iteration)
            gql_query = g.gql['query']
            gql_variables = g.gql['variables']
            gql_test = GqlTest(testTag=t_t,
                               uiTransaction=g.trx_name,
                               variables=gql_variables,
                               gqlQuery=gql_query,
                               operationName=g.gql[OPERATION_NAME])
            gql_tests.append(gql_test)
        # save GQL query to generated dir, use MD5 hash as subdir
        generated_dir = Path(self.output_dir, 'generated')
        for g_t in gql_tests:
            gql_file_dir = Path(generated_dir, f"{g_t.gqlHashMD5}")
            os.makedirs(gql_file_dir, exist_ok=True)
            gql_file_name = Path(gql_file_dir, f"{g_t.operationName}.graphql")
            try:
                with open(gql_file_name, 'w') as gql_file:
                    gql_file.write(g_t.gqlQuery)
            except FileNotFoundError as e:  # in case of invalid file name
                error_print(error=e, message=f"Removing {g_t.operationName}")
                # remove gql with invalid operation name from index.json
                gql_tests.remove(g_t)
        # run the same GQL multiple times, tests are without gql query
        tests_multiple_runs = []  # run the same GQL multiple time
        for g_t in gql_tests:
            for r in range(self.test_runs):
                g_t.testRun = r + 1  # 1 based
                g_t_dict = copy(g_t).__dict__
                # remove GQL query
                g_t_dict.pop('gqlQuery')
                tests_multiple_runs.append(g_t_dict)
        index_file_dir = Path(generated_dir, "index.json")
        with open(index_file_dir, "w") as json_file:
            json.dump(tests_multiple_runs, json_file, indent=4, sort_keys=True)
