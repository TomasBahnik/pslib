from pathlib import Path

from cpt.comparator import Comparator, Measurement

if __name__ == '__main__':
    gql_file_1 = Path('csv/paas_dq/GQLHash_VarLength_OperName.csv')
    trx_file_1 = Path('csv/paas_dq/GQLHash_VarLength_FeTrx.csv')
    gql_file_2 = Path('csv/paas_ci/GQLHash_VarLength_OperName.csv')
    trx_file_2 = Path('csv/paas_ci/GQLHash_VarLength_FeTrx.csv')
    print(f"inputs: {gql_file_1}, {gql_file_2}, {trx_file_1}, {trx_file_2}")
    m_1 = Measurement(gql_file_1, trx_file_1)
    m_2 = Measurement(gql_file_2, trx_file_2)
    output_path = Path('csv')
    print(f"output : {output_path.absolute()}")

    comparator = Comparator(m_1, m_2, ('_paas_dq', '_paas_ci'), output_dir=output_path)
    comparator.merger_gqls()

    comparator = Comparator(m_2, m_1, ('_paas_ci', '_paas_dq'), output_dir=output_path)
    comparator.merger_gqls()
