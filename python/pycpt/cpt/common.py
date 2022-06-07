import os
import re

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

LR_VUGEN_SCRIPT = os.getenv('LR_VUGEN_SCRIPT')

DEBUG_PRINT = False
ERROR_PRINT = True


def debug_print(message, print_debug):
    if print_debug:
        print(message)


def error_print(error: Exception, message: str = ''):
    """error message must be set in order to print error"""
    error_name = error.__class__.__name__
    # do not print key errors
    # is_not_key_error = error_name != 'KeyError'
    message_is_not_empty = len(message) > 1
    debug_print(f"{error_name}:{message}", message_is_not_empty and ERROR_PRINT)


class FeTransaction2Gql:
    def __init__(self, trx_name: str, gql: dict, iteration: int):
        self.trx_name = trx_name
        self.gql: dict = gql
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
