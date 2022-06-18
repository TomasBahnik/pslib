import os
from pathlib import Path

from cpt.common import list_files
from cpt.parse_log import LineProcessor, LogFile
# see https://pyparsing-docs.readthedocs.io/en/latest/
from cpt.parse_rules import ParseResults, request_response_log_rules


def evaluate_logs(log_file: Path, output: Path, name):
    print(f"log file:{log_file.absolute()}")
    print(f"output dir:{output.absolute()}")
    os.makedirs(output, exist_ok=True)
    lp = LineProcessor(request_response_log_rules)
    lf = LogFile(log_file, output, pr=ParseResults(), lp=lp, test_runs=5, log_origin=name)
    lf.parse_save()


if __name__ == '__main__':
    # working dir test
    # set PYTHONPATH=..
    # python parse_logs_test.py
    path = "."
    backups = Path(path)
    logs = list_files(backups)
    for log in logs:
        file_name = log.name.removesuffix('.txt')
        name = file_name if file_name else 'none'
        evaluate_logs(log, Path(backups, name), name=name)
