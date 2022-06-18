import os
from pathlib import Path
from typing import Tuple

import typer

from cpt.comparator import Comparator, Measurement
from cpt.configuration import file_name_logger

VAR_LENGTH_FE_TRX_CSV = "GQLHash_VarLength_FeTrx.csv"
LENGTH_OPER_NAME_CSV = "GQLHash_VarLength_OperName.csv"

app = typer.Typer()
file_name = os.path.basename(__file__).split('.')[0]
logger, log_path = file_name_logger(file_name=file_name)
typer.echo(f"Logging to {log_path}")


@app.command()
def compare_cmd(folder_1: str = typer.Option(...),
                folder_2: str = typer.Option(...),
                suffixes: Tuple[str, str] = ('_1', '_2'), output_dir: str = os.getcwd()):
    """
    compares two measurements
    example (both Windows cmd and Git bash)
    python bin/pycpt/compare_cmd.py --folder-1 bin/pycpt/test/csv/paas_ci --folder-2 bin/pycpt/test/csv/paas_dq
    """
    m1 = Measurement(Path(folder_1, LENGTH_OPER_NAME_CSV), Path(folder_1, VAR_LENGTH_FE_TRX_CSV))
    m2 = Measurement(Path(folder_2, LENGTH_OPER_NAME_CSV), Path(folder_2, VAR_LENGTH_FE_TRX_CSV))
    output_dir = Path(os.getcwd(), output_dir).resolve()
    typer.echo(f"output {output_dir}")
    logger.info(f"output {output_dir}")

    comparator = Comparator(m1, m2, suffixes, output_dir=output_dir)
    comparator.merger_gqls()


if __name__ == "__main__":
    app()
