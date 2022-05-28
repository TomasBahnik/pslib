import json
import os
import re
from datetime import datetime, timedelta

from cpt.graphql import OPERATION_NAME

START_ITER_REGEXP = r"Starting\siteration\s(\d+)"
START_ITER = re.compile(START_ITER_REGEXP)

NOTIFY_TRANSACTION = 'Notify: Transaction'
START_TRX = re.compile(NOTIFY_TRANSACTION + r"\s\"(.*)\"\sstarted")
# ended with a "Pass" status (Duration: 0.8570 Wasted Time: 0.3640)
TRX_COMMON = r"\s\"(.*)\"\sended\swith\sa\s\"(.*)\"\sstatus"
END_TRX = re.compile(NOTIFY_TRANSACTION + TRX_COMMON)
END_TRX_PASSED = re.compile(r".*\(Duration:\s(\d+\.\d+)\sWasted\sTime:\s(\d+\.\d+)\)")
# (Duration: 14.7360 Think Time: 0.0010 Wasted Time: 3.5380)
END_TRX_PASSED_THINK_TIME = \
    re.compile(r".*\(Duration:\s(\d+\.\d+)\sThink\sTime:\s(\d+\.\d+)\sWasted\sTime:\s(\d+\.\d+)\)")
# t=00006915ms
LOG_TIMESTAMP_RE = re.compile(r"t=(\d+)ms")
# Virtual User Script started at : 2020-10-05 11:27:34
SCRIPT_STARTED_RE = re.compile(r"Virtual User Script.+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})")
ELK_URL_FROM_OS = os.getenv('ELK_BASE_URL') if os.getenv('ELK_BASE_URL') else "http://log01a.do.prg-krl.atc:5050"
ELK_BASE_URL = ELK_URL_FROM_OS if ELK_URL_FROM_OS.endswith("/") else ELK_URL_FROM_OS + '/'
# {"operationName":"GetApplicationMode","variables":{}
# TODO operationName -> OPERATION_NAME const can't escape '\' in f strings use """?
# OPERATION_NAME_START = r"{\"operationName\":\"(\w+)\",\"variables\":(\{.*\})"
OPERATION_NAME_START = r"{\"operationName\":\"(\w+)\","
OPERATION_NAME_START_RE = re.compile(OPERATION_NAME_START)

# load steps and actions from output.txt
# used as LOG_TIMESTAMP_RE = re.compile(r"t=(\d+)ms")
# t=00029357ms: Step 21: Click on Browse button started    [MsgId: MMSG-205180]	[MsgId: MMSG-205180]
SCRIPT_STEP_OUTPUT_RE = r't=(\d+)ms:\sStep\s([\d\.]+):\s([a-zA-Z\s"]+[\w"])\s{4}'
SCRIPT_STEP_OUTPUT_RE_COMPILED = re.compile(SCRIPT_STEP_OUTPUT_RE)


class FeTransaction2Gql:
    def __init__(self, trx_name: str, gql: dict, iteration: int):
        self.trx_name = trx_name
        self.gql = gql
        self.iteration = iteration


class FeTransactionGqlCount:
    def __init__(self, trx_name, gql_count, iteration):
        self.trx_name = trx_name
        self.gql_count = gql_count
        self.iteration = iteration

    def __str__(self):
        if self.trx_name is not None:
            return str(self.iteration) + "." + self.trx_name + " : " + str(self.gql_count) + " GQLs"
        else:
            return str(self.iteration) + ".Unassigned : " + str(self.gql_count) + " GQLs"


class FeTransaction:
    def __init__(self, name: str, status: str,
                 end_time: str = '', error: str = '',
                 iteration: int = 0, duration: float = 0,
                 wasted_time: float = 0, think_time: float = 0):
        self.trx_name = name
        self.status = status
        self.duration = duration
        self.think_time = think_time
        self.wasted_time = wasted_time
        self.trx_time = round((duration - wasted_time), 3)
        self.error = error
        self.iteration = iteration
        self.end_time = end_time


def parse_steps(log_file):
    steps = []
    with open(log_file, encoding='windows-1252') as input_file:
        for line in input_file.readlines():
            stripped = line.strip()
            s_s_t = get_script_start_time(stripped)
            match_step = SCRIPT_STEP_OUTPUT_RE_COMPILED.match(stripped)
            if match_step:
                t = int(match_step.group(1))
                t_f = (s_s_t + timedelta(milliseconds=t)).isoformat()
                step = [t_f, match_step.group(2), match_step.group(3)]
                steps.append(step)
    return steps


def parse_transactions(log_file):
    transactions = []
    start_trx_name = None
    iteration = 0
    s_s_t = None
    with open(log_file, encoding='windows-1252') as input_file:
        for line in input_file.readlines():
            stripped = line.strip()
            s_s_t = s_s_t if s_s_t is not None else get_script_start_time(stripped)
            if START_ITER.match(stripped):
                iteration_pattern = START_ITER.match(stripped)
                iteration = int(iteration_pattern.group(1))
                print("start iteration {}".format(iteration))
            if START_TRX.match(stripped):
                start = START_TRX.match(stripped)
                start_trx_name = start.group(1)
                print("start trx {}".format(start_trx_name))
            if END_TRX.match(stripped):
                end = END_TRX.match(stripped)
                end_trx_name = end.group(1)
                end_trx_status = end.group(2)
                if end_trx_name != start_trx_name:
                    print("\tend trx {} does not equals {}!".format(end_trx_name, start_trx_name))
                trx = FeTransaction(end_trx_name, end_trx_status)
                trx.iteration = iteration  # initialized to 0 by default
                print("\tend trx {} : status = {}".format(end_trx_name, end_trx_status))
                if end_trx_status == 'Pass':
                    if END_TRX_PASSED.match(stripped):
                        trx.end_time = fe_trx_end_time(prev_line, s_s_t)
                        durations = END_TRX_PASSED.match(stripped)
                        trx.duration = float(durations.group(1))
                        trx.wasted_time = float(durations.group(2))
                        print("\tend trx {} : duration = {} wasted time = {}"
                              .format(end_trx_name, trx.duration, trx.wasted_time))
                    if END_TRX_PASSED_THINK_TIME.match(stripped):
                        trx.end_time = fe_trx_end_time(prev_line, s_s_t)
                        durations = END_TRX_PASSED_THINK_TIME.match(stripped)
                        trx.duration = float(durations.group(1))
                        trx.think_time = float(durations.group(2))
                        trx.wasted_time = float(durations.group(3))
                        print("\tend trx {} : duration = {} think time = {} wasted time = {}"
                              .format(end_trx_name, trx.duration, trx.think_time, trx.wasted_time))
                elif end_trx_status == "Fail":
                    trx.error = prev_line
                    trx.end_time = fe_trx_end_time(prev_line, s_s_t)
                start_trx_name = None
                transactions.append(trx.__dict__)
            prev_line = stripped  # remember previous line with relative timestamp
    print("transactions size : {}".format(len(transactions)))
    return transactions


def fe_trx_end_time(prev_line: str, script_start_time: datetime):
    t = int(LOG_TIMESTAMP_RE.match(prev_line).group(1)) if LOG_TIMESTAMP_RE.match(prev_line) else -1
    return (script_start_time + timedelta(milliseconds=t)).isoformat()


def get_script_start_time(line: str) -> datetime:
    match = SCRIPT_STARTED_RE.match(line)
    if match:
        str_dt = match.group(1)
        return datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")


def parse_graphql(log_file):
    trx_gqls = []
    fe_trx = []
    iteration = None
    line_number = 0
    removed_trx = None
    with open(log_file, encoding='windows-1252') as input_file:
        for line in input_file.readlines():
            line_number += 1
            stripped = line.strip()
            if START_ITER.match(stripped):
                iteration_pattern = START_ITER.match(stripped)
                iteration = iteration_pattern.group(1)
                print("start iteration {}".format(iteration))
            if START_TRX.match(stripped):
                start = START_TRX.match(stripped)
                start_trx = start.group(1)
                fe_trx.append(start_trx)
                if len(fe_trx) > 1:
                    print("Line {}. Adding start trx : {}, transaction list : {} transaction list size {}"
                          .format(line_number, start_trx, fe_trx, len(fe_trx)))
                else:
                    print("Line {}. Adding start trx : {}, transaction list : {}"
                          .format(line_number, start_trx, fe_trx))
                t_name = fe_trx[-1]
                print("Last trx : name = {}".format(t_name))
            if END_TRX.match(stripped):
                end = END_TRX.match(stripped)
                end_trx = end.group(1)
                end_trx_status = end.group(2)
                print(
                    "Line {}. Resolving end trx {} ended with {} status.".format(line_number, end_trx, end_trx_status))
                t_name = fe_trx[-1]
                if end_trx != t_name:
                    print("\tCurrent end trx '{}' IS NOT EQUAL to the last trx '{}'!".format(end_trx, t_name))
                # try 2nd to last
                if len(fe_trx) > 1 and end_trx != t_name:
                    t_name = fe_trx[-2]  # next to last
                    print('\tMore than 1 started trx : {}'.format(fe_trx))
                    # if names are equal remove 2nd to last item from list
                    if end_trx == t_name:
                        print("\t{} IS EQUAL to next to last trx '{}'. Remove it from transaction list"
                              .format(end_trx, t_name))
                        removed_trx = fe_trx.pop(-2)
                        print("Removed {}. Current transaction list {} has size {}"
                              .format(removed_trx, fe_trx, len(fe_trx)))
                else:
                    removed_trx = fe_trx.pop()  # default last
                    print("Trx {} ended. Remove it from list. Current transaction list {} has size {}"
                          .format(removed_trx, fe_trx, len(fe_trx)))
            if stripped.startswith('{"' + OPERATION_NAME + '"'):
                stripped = stripped.replace('\\\\', '\\')
                # when created by cmd line version
                if "\t" in stripped:
                    tab = stripped.index("\t")
                    stripped = stripped[0:tab]
                gql = json.loads(stripped)
                if len(fe_trx) == 0:
                    o_name = gql[OPERATION_NAME]
                    print("\tLine {}. {} : CANNOT ASSIGN GQL to transaction. Transaction list is empty !!"
                          .format(line_number, o_name))
                    print("\tLine {}. {}:{} Assigning last removed trx".format(line_number, removed_trx, o_name))
                    trx_gql = FeTransaction2Gql(removed_trx, gql, iteration)
                else:
                    t_name = fe_trx[-1]
                    o_name = gql[OPERATION_NAME]
                    print("\t{}:{}".format(t_name, o_name))
                    trx_gql = FeTransaction2Gql(t_name, gql, iteration)
                # TODO init action iteration 0 or -1
                if trx_gql.iteration is not None:
                    trx_gqls.append(trx_gql)
    gql_counts = fe_trans_gql_count(trx_gqls)
    for i in gql_counts:
        print(i)
    print("trx_gqls size : {}".format(len(trx_gqls)))
    return trx_gqls


def fe_trans_gql_count(fe_trx2gqls):
    ret_val = []
    fe_transactions = {trx_gql.trx_name for trx_gql in fe_trx2gqls}
    fe_iterations = {trx_gql.iteration for trx_gql in fe_trx2gqls}
    for i in sorted(fe_iterations):
        for fe_trx in fe_transactions:
            trx_gql_count = [x for x in fe_trx2gqls if (x.trx_name == fe_trx and int(x.iteration) == int(i))]
            gql_count = len(trx_gql_count)
            item = FeTransactionGqlCount(fe_trx, gql_count, i)
            ret_val.append(item)
    return ret_val
