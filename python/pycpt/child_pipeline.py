import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

import typer

from cpt.common import list_files, archive_folder
from cpt.configuration import file_name_logger, Configuration
from cpt.parse_log import LineProcessor, LogFile
from cpt.parse_rules import ParseResults, request_response_log_rules

app = typer.Typer()
file_name = os.path.basename(__file__).split('.')[0]
logger: logging.Logger
log_path: Path


def process_screenshots(cfg: Configuration, output_dir: Path, test: str = None):
    scripts_dir = cfg.get_property('lr.vugen.scripts.git.dir')
    test_dir = Path(scripts_dir, test)
    logger.info(f"screenshots from {test}")
    s_s_s = list_files(Path(scripts_dir, test), file_type='.png')
    s_s_dir = Path(output_dir, 'screenshots')
    os.makedirs(s_s_dir, exist_ok=True)
    for s_s in s_s_s:
        shutil.copy(Path(test_dir, s_s), s_s_dir)


def run_api_tests(cfg: Configuration, backup_path: Path, log_base_dir: str, test_suite: str = 'generated'):
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    os.makedirs(Path(log_base_dir), exist_ok=True)
    typer.echo(f"api test logging to: {log_base_dir}: {test_suite}.log, api_test_{test_suite}.log")
    test_options: List[str] = [f"-Dtest.environment={test_env}",
                               f"-Dlogger.base.dir={log_base_dir}/",
                               f"-Dlogger.file.name={test_suite}.log",
                               f"-PsuiteFile={cfg.get_property('test.suite.rel.dir')}/{test_suite}.xml",
                               f"-PexcludeTests=**/*DataGen*"]
    cmd = ['gradlew.bat', 'test'] + test_options
    f = open(Path(log_base_dir, f'api_test_{test_suite}.log'), "w")
    p = subprocess.Popen(cmd, stdout=f)
    ret = p.wait()
    logger.info(f"{cmd} ended by {ret}")
    test_results = cfg.get_property('test.results.rel.dir')
    t_r_path = Path(test_results).resolve()
    # TODO same as check_output - unify
    if t_r_path.exists():
        p = archive_folder(src_path=t_r_path, dest_path=backup_path,
                           dest_base_file_name='test_results')
        logger.info(f"Test results {t_r_path} backup with return code {p.returncode}")
        if p.returncode == 0:
            logger.info(f"backup returned {p.returncode}. Remove {t_r_path}")
            shutil.rmtree(t_r_path)


def run_fe_tests(cfg: Configuration, output_path: Path, backup_path: Path):
    tests: List[str] = cfg.get_property('lr.vugen.scripts').split(',')
    fe_app_url = cfg.get_property('fe.app.url')
    scripts_dir = cfg.get_property('lr.vugen.scripts.git.dir')
    for test in tests:
        check_output(backup_path, output_path)
        test_dir = Path(scripts_dir, test)
        test_usr = Path(test_dir, test + '.usr').resolve()
        cmd = ['mdrv.exe', '-usr', f"{test_usr}", '-app_url', fe_app_url]
        cmd_open_wait(cmd)
        log_file = Path(test_dir, 'output.txt')
        if log_file.exists():
            process_fe_log(log_file, output_dir=output_path, log_origin=test)
            shutil.copy(log_file, output_path)
            # copy screenshots
            process_screenshots(cfg, output_dir=output_path, test=test)
        else:
            m = f"{log_file} does not exist"
            logger.error(m)
            typer.echo(m)
        p = archive_folder(src_path=output_path, dest_path=backup_path, dest_base_file_name=test)
        logger.info(f"{test} archived with return code {p.returncode}")


def cmd_open_wait(cmd):
    m = f"Start {cmd} in {os.getcwd()}"
    logger.info(m)
    typer.echo(m)
    p = subprocess.Popen(cmd)
    ret = p.wait()
    m = f"{cmd} return code={ret}"
    logger.info(m)
    typer.echo(m)
    return ret


def check_output(backup_path, output_path):
    """backup existing output dir before new test"""
    if output_path.exists():
        logger.info(f"Backup {output_path} - it exists")
        p = archive_folder(src_path=output_path, dest_path=backup_path, dest_base_file_name="before_test")
        if p.returncode == 0:
            logger.info(f"backup returned {p.returncode}. Remove {output_path}")
            shutil.rmtree(output_path)


def process_fe_log(log_file: Path, output_dir: Path, log_origin: str):
    lp = LineProcessor(request_response_log_rules)
    lf = LogFile(log_file, output_dir, pr=ParseResults(), lp=lp, test_runs=5, log_origin=log_origin)
    lf.parse_save()


@app.command()
def child_pipeline(test_env: str = typer.Option(..., help="Test environment", envvar="TEST_ENV"),
                   step: str = typer.Option(...)):
    global logger
    global log_path
    log_folder = Path(f"log/{test_env}").resolve()
    logger, log_path = file_name_logger(folder=str(log_folder), file_name=file_name)
    typer.echo(f"Logging to {log_path}")
    cfg = Configuration(test_env=test_env)
    # run_tests = cfg.get_property('run.fe.tests')
    gen_data_dir = cfg.get_property("generated.data.rel.dir")
    backup_dir = cfg.get_property("backup.data.rel.dir")
    # full paths
    gen_data_path = Path(gen_data_dir).resolve()
    backup_path = Path(backup_dir).resolve()

    match step:
        case 'fe_tests':
            run_fe_tests(cfg, output_path=gen_data_path, backup_path=backup_path)
        case 'api_tests':
            run_api_tests(cfg, backup_path=backup_path, log_base_dir=str(log_folder))
        case _:
            logger.error(f"Unknown step {step}")


if __name__ == "__main__":
    app()
