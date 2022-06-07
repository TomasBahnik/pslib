import argparse
import sys
from pathlib import Path

from cpt.comparator import Comparator, Measurement


def setup_arg_parser():
    p = argparse.ArgumentParser(description='Search and replace variables in Kustomize k8s manifets.')
    p.add_argument('--gql_file_1', type=str, required=True,
                   help='location of gql csv file')
    p.add_argument('--trx_file_1', type=str, required=True,
                   help='location fe transaction csv')
    p.add_argument('--gql_file_2', type=str, required=True,
                   help='location of gql csv file')
    p.add_argument('--trx_file_2', type=str, required=True,
                   help='location fe transaction csv')
    return p


if __name__ == '__main__':
    parser = setup_arg_parser()
    args = parser.parse_args()

    gql_file_1 = Path(args.gql_file_1)
    trx_file_1 = Path(args.trx_file_1)

    gql_file_2 = Path(args.gql_file_2)
    trx_file_2 = Path(args.trx_file_2)

    measurement_1 = Measurement(gql_file_1, trx_file_1)
    measurement_2 = Measurement(gql_file_2, trx_file_2)
    output_dir = Path('compare')

    comparator = Comparator(measurement_1, measurement_2, ('_permissions', '_release'), output_dir=output_dir)
    comparator.merger_gqls()

    comparator = Comparator(measurement_2, measurement_1, ('_release', '_permissions'), output_dir=output_dir)
    comparator.merger_gqls()
    sys.exit(0)
