from pathlib import Path

from cpt.configuration import Configuration
from cpt.kustomize import KubernetesManifest, kustomize_build, git_checkout

if __name__ == '__main__':
    TEST_ENV = "paas_ci"
    p = Configuration(test_env=TEST_ENV)

    KUSTOMIZATION_YAML = 'kustomization.yaml'
    GENERIC_FILE = p.get_property('kustomize.generic.file')
    INTERPOLATED_FILE = p.get_property('kustomize.interpolated.file')
    KUST_GIT_DIR = p.get_property('kustomize.git.dir')
    # KUST_BUILDS_DIR = f"{os.getcwd()}\\kustomize_builds"
    KUST_BUILDS_DIR = p.get_property('kustomize.build.dir')
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
