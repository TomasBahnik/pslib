import argparse
from pathlib import Path

from cpt.parse_log import LogFile, LineProcessor
from cpt.parse_rules import ParseResults, request_response_log_rules


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Search and replace variables in Kustomize k8s manifets.')
    parser.add_argument('--log_file', type=str, required=True,
                        help='location of frontend log file')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='location artifacts produced by processing the frontend log')
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('-gql', help='extract individual GQLs', action='store_true')
    mutex_group.add_argument("-trx", help="extract individual frontend transactions", action='store_true')
    return parser


if __name__ == '__main__':
    parser = setup_arg_parser()
    args = parser.parse_args()

    log_file = Path(args.log_file)
    output_dir = Path(args.output_dir)
    print(f"log file:{log_file.absolute()}")
    print(f"output dir:{output_dir.absolute()}")

    pr = ParseResults()
    lp = LineProcessor(request_response_log_rules)
    lf = LogFile(log_file, output_dir, pr=pr, lp=lp)

    lf.parse_all()
    if args.trx:
        lf.print_fe_transactions()
    elif args.gql:
        lf.print_gqls()
    else:
        print(f'Unknown target')
