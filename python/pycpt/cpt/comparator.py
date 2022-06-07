from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd
from pandas import DataFrame

VAR_LENGTH_COLUMN = 'Var Length'
GQL_HASH_COLUMN = 'GQL Hash'
MEAN = 'Avg Duration [ms]'


@dataclass
class Measurement:
    gql_varlen_on: Path
    gql_varlen_fe: Path
    df_gvo: DataFrame = None
    df_gvf: DataFrame = None

    def __post_init__(self):
        self.df_gvo = pd.read_csv(self.gql_varlen_on)
        self.df_gvf = pd.read_csv(self.gql_varlen_fe)


class Comparator:
    """ Kibana raw csv"""

    def __init__(self, m1: Measurement, m2: Measurement, suffixes: Tuple[str, str], output_dir: Path):
        drop_cols_gvo1 = [4, 5, 7, 8]
        drop_cols_gvo2 = [2, 4, 5, 7, 8]
        self.m1 = m1
        self.m2 = m2
        self.suffixes = suffixes
        self.output_dir = output_dir
        self.drop_labels_gvo1 = self.m1.df_gvo.columns[drop_cols_gvo1]
        self.drop_labels_gvo2 = self.m2.df_gvo.columns[drop_cols_gvo2]

    def merger_gqls(self):
        df1 = self.m1.df_gvo.drop(self.drop_labels_gvo1, axis=1, inplace=False)
        df2 = self.m2.df_gvo.drop(self.drop_labels_gvo2, axis=1, inplace=False)
        m = pd.merge(df1, df2, how='outer', on=[GQL_HASH_COLUMN, VAR_LENGTH_COLUMN], suffixes=self.suffixes)
        ratio_avg = m[MEAN + self.suffixes[0]] / m[MEAN + self.suffixes[1]]
        ratio_avg_col = 'ratio avg'
        m[ratio_avg_col] = ratio_avg
        m['diff avg [%]'] = (ratio_avg - 1).round(2) * 100.0
        m.sort_values(by=ratio_avg_col, ascending=False, inplace=True)
        out_file_md = f"{self.output_dir}/comparison{self.suffixes[0]}_vs_{self.suffixes[1]}.md"
        out_file_csv = f"{self.output_dir}/comparison{self.suffixes[0]}_vs_{self.suffixes[1]}.csv"
        m.round(2).to_markdown(out_file_md, index=False)
        m.round(2).to_csv(out_file_csv, index=False)
