import os
import subprocess
from pathlib import Path

from cpt.configuration import Configuration
from cpt.kustomize import KubernetesManifest


def kustomize_build(build_dir: Path, git_dir: Path, subfolder: str, output_file: str):
    output_file_path = Path(build_dir, subfolder, output_file)
    with open(output_file_path, "w") as outfile:
        build_cmd = ['kustomize', 'build', str(git_dir.absolute())]
        print(f"running {build_cmd} in {os.getcwd()}")
        p = subprocess.run(build_cmd, stdout=outfile, stderr=subprocess.PIPE)
        error = p.stderr
        print(f"{p}\nerror {error}")


def kustomize_deploy(deploy_file: Path):
    cmd = ['kustomize', 'apply', '-f',  str(deploy_file)]
    p = subprocess.run(cmd, stdout=subprocess.STDOUT, stderr=subprocess.PIPE)
    error = p.stderr
    print(f"{p}\nerror {error}")


def git_checkout(git_dir: Path, file: str):
    cwd = os.getcwd()
    os.chdir(git_dir)
    subprocess.Popen(['git', 'checkout', file])
    os.chdir(cwd)


if __name__ == '__main__':
    resources = Path(os.getcwd(), '..', '..', '..', 'modules', 'api-tests', 'resources').resolve()
    TEST_ENV = "paas_ci"
    p = Configuration(resources, TEST_ENV)
    p.set_raw_properties()
    p.set_properties()

    GENERIC_FILE = p.properties['kustomize.generic.file']
    INTERPOLATED_FILE = p.properties['kustomize.interpolated.file']
    KUSTOMIZATION_YAML = 'kustomization.yaml'
    KUST_GIT_DIR = p.properties['kustomize.git.dir']
    # KUST_BUILDS_DIR = f"{os.getcwd()}\\kustomize_builds"
    KUST_BUILDS_DIR = p.properties['kustomize.build.dir']
    FOLDER = f"{TEST_ENV}_latest"

    km = KubernetesManifest(KUST_BUILDS_DIR, KUST_GIT_DIR, FOLDER,
                            test_env=TEST_ENV,
                            generic_m=GENERIC_FILE,
                            interpolated_m=INTERPOLATED_FILE)
    km.switch_loaded_config_map()
    kustomize_build(Path(KUST_BUILDS_DIR), Path(KUST_GIT_DIR), FOLDER, GENERIC_FILE)
    git_checkout(Path(KUST_GIT_DIR), KUSTOMIZATION_YAML)
    km.load_vars()
    km.load_manifest()
    km.save_sizing()
