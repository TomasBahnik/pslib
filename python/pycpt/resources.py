import argparse
import os
from pathlib import Path

from cpt.configuration import Configuration
from cpt.kustomize import KubernetesManifest, kustomize_build, git_checkout


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Search and replace variables in Kustomize k8s manifets.')
    parser.add_argument('--subfolder', type=str, required=True,
                        help='env specific subfolder in kustomize build directory')
    return parser


if __name__ == '__main__':
    args = setup_arg_parser().parse_args()
    test_env = os.getenv("TEST_ENV")
    subfolder_args = args.subfolder

    # load properties for given test env
    # cwd = CPT_HOME
    p = Configuration(test_env=test_env)
    p.set_raw_properties()
    p.set_properties()

    # get required properties
    builds_dir = p.get_property('kustomize.build.dir')
    git_dir = p.get_property('kustomize.git.dir')
    generic_file = p.get_property('kustomize.generic.file')
    interpolated_file = p.get_property('kustomize.interpolated.file')

    km = KubernetesManifest(builds_dir, git_dir, subfolder_args,
                            test_env=test_env, generic_m=generic_file,
                            interpolated_m=interpolated_file)
    km.switch_loaded_config_map()
    kustomize_build(Path(builds_dir), Path(git_dir), subfolder_args, generic_file)
    git_checkout(Path(git_dir), 'kustomization.yaml')
    km.load_vars()
    km.load_manifest()
    km.save_sizing()
