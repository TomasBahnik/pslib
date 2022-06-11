from pathlib import Path

from cpt.comparator import Comparator, Measurement


def compare_folders(f1, f2):
    gql_csv = 'GQLHash_VarLength_OperName.csv'
    fe_csv = 'GQLHash_VarLength_FeTrx.csv'
    gql_file_1 = Path('csv', f1, gql_csv)
    trx_file_1 = Path('csv', f1, fe_csv)
    gql_file_2 = Path('csv', f2, gql_csv)
    trx_file_2 = Path('csv', f2, fe_csv)
    print(f"inputs: {gql_file_1}, {gql_file_2}, {trx_file_1}, {trx_file_2}")
    m1 = Measurement(gql_file_1, trx_file_1)
    m2 = Measurement(gql_file_2, trx_file_2)
    output_path = Path('csv')
    print(f"output : {output_path.absolute()}")
    comparator = Comparator(m1, m2, (f'_{f1}', f'_{f2}'), output_dir=output_path)
    comparator.merger_gqls()
    comparator = Comparator(m2, m1, (f'_{f2}', f'_{f1}'), output_dir=output_path)
    comparator.merger_gqls()


if __name__ == '__main__':
    folder_1 = 'paas_dq'
    folder_2 = 'paas_ci'
    compare_folders(folder_1, folder_2)
