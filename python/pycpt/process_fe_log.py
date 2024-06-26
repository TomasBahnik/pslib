import argparse
import os
from pathlib import Path

from cpt.parse_log import LogFile, LineProcessor
from cpt.parse_rules import ParseResults, request_response_log_rules


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Search and replace variables in Kustomize k8s manifets.')
    parser.add_argument('--log_file', type=str, required=True,
                        help='location of frontend log file')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='location artifacts produced by processing the frontend log')
    parser.add_argument('--log_origin', type=str, required=True,
                        help='source of the log file e.g. Vugen script name')
    return parser


if __name__ == '__main__':
    """
    test run : python process_fe_log.py --log_file test/output.txt --output_dir test -trx
    options:
        -trx : extract frontend transactions from log file 
        -gql : extract graphql requests from log file
    """
    parser = setup_arg_parser()
    args = parser.parse_args()

    log_file = Path(args.log_file)
    output_dir = Path(args.output_dir)
    log_origin = args.log_origin

    print(f"log file:{log_file.absolute()}")
    print(f"output dir:{output_dir.absolute()}")
    print(f"log origin:{log_origin}")

    # origin of output file - exposed by shell scripts
    # TODO oring of parsed file passed as argument from calling shell script
    # e.g. bin/lr_vugen_test.sh:process_vugen_log()
    vugen_script = os.getenv('LR_VUGEN_SCRIPT')
    lp = LineProcessor(request_response_log_rules)
    lf = LogFile(log_file, output_dir, pr=ParseResults(), lp=lp, test_runs=5, log_origin=log_origin)
    lf.parse_save()
