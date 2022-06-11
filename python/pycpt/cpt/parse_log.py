""" Frontend test logs http communication. Parsing that log provides GQL calls and timing for further analyses"""
import datetime
import hashlib
import json
import os
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Any

from cpt.configuration import setup_logging, fullname
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
                 log_origin: str = 'fe'):
        self.log_file = log_file
        self.output_dir = output_dir
        self.pr = pr
        self.lp = lp
        self.test_runs = test_runs
        self.log_origin = log_origin
        # successfully extracted and saved GQL tests
        self.gql_tests: List[GqlTest] = []
        # actual set of GQL tests stored in index.json
        self.multiplied_gql_tests: List[dict] = []
        self.n_gql_test: dict = {}
        self.logger = setup_logging(fullname(self))
        self.create_dir()

    def create_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

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
        summary_file_name = Path(self.output_dir, f"{self.log_origin}_summary")
        with open("{}.json".format(summary_file_name), "w") as json_file:
            json.dump(fe_trx_dict, json_file, indent=4, sort_keys=True)
        html = fe_transaction_html_template().render(trxs=fe_trx_dict)
        with open("{}.html".format(summary_file_name), "w") as html_file:
            html_file.write(html)

    def save_elk_events(self):
        file_name = Path(self.output_dir, f"{self.log_origin}_feElkEvents.json")
        with open(file_name, "w") as json_file:
            json.dump(self.pr.fe_elk_events, json_file, indent=4, sort_keys=True)

    def fe_transaction_elk(self):
        """Prepares and sends ELK events for fe transaction"""
        self.pr.set_gql_counts()
        self.pr.set_fe_elk_events()
        self.save_elk_events()

    def prepare_gql_tests(self):
        test_tag = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        for g in self.pr.fet_iter_gql:
            t_t = test_tag + "_" + str(g.iteration)
            gql_query = g.gql['query']
            gql_variables = g.gql['variables']
            gql_test = GqlTest(testTag=t_t,
                               uiTransaction=g.trx_name,
                               variables=gql_variables,
                               gqlQuery=gql_query,
                               operationName=g.gql[OPERATION_NAME])
            self.gql_tests.append(gql_test)

    def save_gql_tests(self):
        """
        Save GQL query to output dir, use MD5 hash as subdir. If obscure filename (operationName)
        appears remove that GQL
        """
        self.logger.info(f"Saving {len(self.gql_tests)} GQL test to {self.output_dir} dir")
        for g_t in self.gql_tests:
            gql_file_dir = Path(self.output_dir, f"{g_t.gqlHashMD5}")
            os.makedirs(gql_file_dir, exist_ok=True)
            gql_file_name = Path(gql_file_dir, f"{g_t.operationName}.graphql")
            try:
                with open(gql_file_name, 'w') as gql_file:
                    gql_file.write(g_t.gqlQuery)
            except FileNotFoundError as e:  # in case of invalid file name
                self.logger.error(f"Removing {g_t.operationName}")
                # remove gql with invalid operation name from index.json
                self.gql_tests.remove(g_t)

    def multiply_gql_tests(self):
        """ Run the same GQL multiple times to get better stats """
        self.logger.info(f"Multiplying {len(self.gql_tests)} GQL test by {self.test_runs}")
        for g_t in self.gql_tests:
            for r in range(self.test_runs):
                tmp_g_t = copy(g_t)
                tmp_g_t.testRun = r + 1  # 1 based
                tmp_dict = tmp_g_t.__dict__
                tmp_dict.pop('gqlQuery')
                self.multiplied_gql_tests.append(tmp_g_t.__dict__)

    def save_index(self):
        index_file = Path(self.output_dir, "index.json")
        self.logger.info(f"Saving index with {len(self.multiplied_gql_tests)} GQL test to {index_file}")
        with open(index_file, "w") as json_file:
            json.dump(self.multiplied_gql_tests, json_file, indent=4, sort_keys=True)

    def count_gql_tests(self):
        for g_t in self.multiplied_gql_tests:
            g_hash = g_t["gqlHashMD5"]
            v_hash = g_t["variablesHashMD5"]
            v_length = g_t["variablesLength"]
            o_n = g_t["operationName"]
            try:
                self.n_gql_test[g_hash]
            except KeyError as e:
                self.n_gql_test[g_hash] = {}
                self.n_gql_test[g_hash]["operationName"] = o_n
            try:
                self.n_gql_test[g_hash][v_length]
            except KeyError as e:
                self.n_gql_test[g_hash][v_length] = 0
            try:
                self.n_gql_test[g_hash][v_hash]
            except KeyError as e:
                self.n_gql_test[g_hash][v_hash] = 0

            self.n_gql_test[g_hash][v_hash] += 1
            self.n_gql_test[g_hash][v_length] += 1

        index_file = Path(self.output_dir, "gql_counts.json")
        with open(index_file, "w") as json_file:
            json.dump(self.n_gql_test, json_file, indent=4)

    def save_gqls(self):
        self.prepare_gql_tests()
        self.save_gql_tests()
        self.multiply_gql_tests()
        self.count_gql_tests()
        self.save_index()
