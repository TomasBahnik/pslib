import datetime
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

import time
import typer

from cpt.configuration import Configuration, file_name_logger

# dynamically added property
DEPLOY_FOLDER = "deploy_folder"

app = typer.Typer()
file_name = os.path.basename(__file__).split('.')[0]
logger, log_path = file_name_logger(file_name=file_name)
typer.echo(f"Logging to {log_path}")


def git_checkout(git_dir: str = None, file: str = None):
    cwd = os.getcwd()
    os.chdir(Path(git_dir))
    logger.info(f"git checkout {file} in {os.getcwd()}")
    subprocess.Popen(['git', 'checkout', file], stdout=subprocess.PIPE)
    os.chdir(cwd)


def kustomize_build(build_dir: Path, git_dir: Path, subfolder: str, output_file: str):
    output_file_path = Path(build_dir, subfolder, output_file)
    with open(output_file_path, "w") as outfile:
        build_cmd = ['kustomize', 'build', str(git_dir.absolute())]
        message = f"running {build_cmd}"
        logger.info(message)
        p = subprocess.run(build_cmd, stdout=outfile, stderr=subprocess.PIPE)
        logger.error(p.stderr)


def build_deployment(cfg: Configuration):
    from cpt.kustomize import KubernetesManifest

    # read properties for given test env
    builds_dir = cfg.get_property('kustomize.build.dir')
    git_dir = cfg.get_property('kustomize.git.dir')
    generic_file = cfg.get_property('kustomize.generic.file')
    interpolated_file = cfg.get_property('kustomize.interpolated.file')
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    deploy_folder = cfg.get_property(DEPLOY_FOLDER)

    backup_folder(builds_dir, deploy_folder)

    # for sake of right initial state
    git_checkout(git_dir, file='kustomization.yaml')

    km = KubernetesManifest(builds_dir, git_dir, deploy_folder,
                            test_env=test_env, generic_m=generic_file,
                            interpolated_m=interpolated_file)
    km.switch_loaded_config_map()
    kustomize_build(Path(builds_dir), Path(git_dir), deploy_folder, generic_file)
    # revert changes
    git_checkout(git_dir, 'kustomization.yaml')

    km.load_vars()
    km.load_manifest()
    km.save_sizing()


def backup_folder(top_dir, folder):
    src_folder = Path(top_dir, folder)
    if src_folder.is_dir():
        dt = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        dest_folder = str(src_folder) + '_' + dt
        logger.info(f"Backup {src_folder} to {Path(dest_folder)}")
        os.rename(src_folder, Path(dest_folder))


def deploy_app(cfg: Configuration):
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    builds_dir = cfg.get_property('kustomize.build.dir')
    interpolated_file = cfg.get_property('kustomize.interpolated.file')
    deploy_file = Path(builds_dir, f"{test_env}_latest", interpolated_file)
    logger.info(f"{test_env}:Deploy app from {deploy_file}")
    cmd = ['kubectl', 'apply', '-f', str(deploy_file)]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.error(p.stderr)


def delete_app(cfg: Configuration):
    builds_dir = cfg.get_property('kustomize.build.dir')
    interpolated_file = cfg.get_property('kustomize.interpolated.file')
    deploy_folder = cfg.get_property(DEPLOY_FOLDER)
    deploy_path = Path(builds_dir, deploy_folder)
    deploy_file = Path(deploy_path, interpolated_file)
    logger.info(f"Delete app from {deploy_file}")
    if deploy_file.exists():
        logger.info(f"Backup {deploy_file}")
        shutil.copy(deploy_file, Path(deploy_path, f'{interpolated_file}.bak'))
    cmd = ['kubectl', 'delete', '-f', str(deploy_file)]
    p = subprocess.run(cmd, stdout=subprocess.STDOUT, stderr=subprocess.PIPE)
    logger.error(p.stderr.decode('utf-8').strip())
    time.sleep(30)
    cmd = ['kubectl', '-n', 'product', 'get', 'pods']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info(p.stdout.decode('utf-8').strip())
    typer.echo(p.stdout.decode('utf-8').strip())


def psql_options(cfg: Configuration, pg_database: str = 'postgres') -> List[str]:
    pg_port = cfg.get_property('db.port')
    pg_host = cfg.get_property('db.host')
    pg_user = cfg.get_property('app.db.user')
    pg_role = cfg.get_property('app.db.role')
    pg_password = cfg.get_property('app.db.password')
    os.putenv('PGPASSWORD', pg_password)
    db_options = ['-d', pg_database]
    pg_options = ['-h', pg_host, '-p', pg_port, '-U', pg_user]
    return db_options + pg_options


def psql_cmd(options: List[str], sql_folder: str = 'sql', sql_file: str = None):
    cmd = ['psql'] + options
    sql_path = Path(os.getcwd(), sql_folder).resolve()
    if sql_file:
        file_option = ['-f', str(Path(sql_path, sql_file).resolve())]
        cmd = cmd + file_option
    logger.info(f"Run psql {cmd}")
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    logger.info(p.stdout)
    typer.echo(p.stdout)


def delete_p_v(cfg: Configuration):
    get_pvc = ['kubectl', 'get', 'pvc', '--no-headers', '-n', 'product']
    get_pvc_name = ['cut', '-d', ' ', '-f', '1']
    del_pvc_cmd = ['kubectl', 'delete', 'pvc', '-n', 'product']
    p1 = subprocess.Popen(get_pvc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.run(get_pvc_name, stdin=p1.stdout, stdout=subprocess.PIPE)
    pvcs: List[str] = p2.stdout.decode('utf-8').strip().split('\n')
    del_pvs = [x for x in pvcs if 'dpe' in x or 'opendistro-es' in x]
    for pv in del_pvs:
        logger.info(f"{del_pvc_cmd + [pv]}")
        # subprocess.run(del_pvc_cmd + [pv])
    time.sleep(10)


def safe_net(cfg: Configuration):
    """ ensure that correct (i.e. equal to test env) k8s context is used """
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    logger.info(f"{test_env}:Safe net")
    # kube.context is set as property for given test env
    kube_context = cfg.get_property("kube.context")
    current_context_cmd = ['kubectl', 'config', 'current-context']
    p = subprocess.run(current_context_cmd, stdout=subprocess.PIPE)
    cc = p.stdout.decode('utf-8').strip()
    typer.echo(f"current context:{cc}")
    use_context_cmd = ['kubectl', 'config', 'use-context', kube_context]
    subprocess.run(use_context_cmd)
    p = subprocess.run(current_context_cmd, stdout=subprocess.PIPE)
    cc = p.stdout.decode('utf-8').strip()
    typer.echo(f"current context:{cc}")
    # by convention k8s context == test env
    assert cc == test_env


def clean_db(cfg: Configuration):
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    logger.info(f"{test_env}: Drop and create all DBs")
    # sql/postgresql/clean_dbs.sql
    # default db is postgres
    opt = psql_options(cfg)
    psql_cmd(opt, sql_folder='sql/postgresql', sql_file='clean_dbs.sql')


def set_jdbc_string(cfg: Configuration):
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    logger.info(f"{test_env}Set correct host name for connections")


def restore_dump(cfg: Configuration):
    test_env = cfg.get_property(Configuration.TEST_ENV_KEY)
    logger.info(f"{test_env}:Restore DB dump")


def build_deploy(cfg):
    build_deployment(cfg)
    deploy_app(cfg)


def new_deploy(cfg):
    delete_app(cfg)
    delete_p_v(cfg)
    build_deploy(cfg)


def clean_deploy(cfg):
    delete_app(cfg)
    delete_p_v(cfg)
    clean_db(cfg)
    build_deploy(cfg)


@app.command()
def redeploy_paas(test_env: str = typer.Option(..., help="Test environment", envvar="TEST_ENV"),
                  step: str = None):
    """
    Provides both individual and aggregated steps to redeploy Kustomize based deployment
    example : python bin/pycpt/redeploy_paas.py --test-env paas_ci --step new_deploy
    expects cwd = CPT_PATH when loading resources
    """
    folder = f"{test_env}_latest"
    cfg = Configuration(test_env=test_env)
    # subfolder under builds_dir = cfg.get_property('kustomize.build.dir')
    cfg.add_property(DEPLOY_FOLDER, folder)

    safe_net(cfg)
    match step:
        case 'build':
            build_deployment(cfg)
        case 'deploy':
            deploy_app(cfg)
        case 'del_app':
            delete_app(cfg)
        case 'del_pv':
            delete_p_v(cfg)
        case 'clean_db':
            clean_db(cfg)
        case 'set_jdbc':
            set_jdbc_string(cfg)
        case 'restore_db':
            restore_dump(cfg)
        case 'new_deploy':
            new_deploy(cfg)
        case 'clean_deploy':
            clean_deploy(cfg)
        case 'build_deploy':
            build_deploy(cfg)
        case 'psql':
            # default value of pg_database=postgres
            opt = psql_options(cfg, pg_database=cfg.get_property('app.db.name'))
            psql_cmd(opt, sql_file='mmm_db_metrics.sql')
        case _:
            logger.error(f"Unknown step {step}")


if __name__ == "__main__":
    app()
