import os
from pathlib import Path
from typing import List

from cpt.parse_log import LineProcessor, LogFile
# see https://pyparsing-docs.readthedocs.io/en/latest/
from cpt.parse_rules import ParseResults, request_response_log_rules


def load_logs(folder: Path, file_type: str = '.txt'):
    # traverse root directory, and list directories as dirs and files as files
    log_files: List[Path] = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.txt'):
                l_f = Path(root, file)
                log_files.append(l_f)
    return log_files


def evaluate_logs(log_file: Path, output: Path, name):
    print(f"log file:{log_file.absolute()}")
    print(f"output dir:{output.absolute()}")
    os.makedirs(output, exist_ok=True)
    pr = ParseResults()
    lp = LineProcessor(request_response_log_rules)
    lf = LogFile(log_file, output, pr=pr, lp=lp, test_runs=5, log_origin=name)

    lf.parse_all()
    lf.save_fe_transactions()
    lf.fe_transaction_elk()
    lf.save_gqls()


if __name__ == '__main__':
    # working dir test
    # set PYTHONPATH=..
    # python parse_logs_test.py
    path = "."
    backups = Path(path)
    logs = load_logs(backups)
    for log in logs:
        file_name = log.name.removesuffix('.txt')
        name = file_name if file_name else 'none'
        evaluate_logs(log, Path(backups, name), name=name)
