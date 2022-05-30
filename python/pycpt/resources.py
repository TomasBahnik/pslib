import argparse
import os
from pathlib import Path

from cpt.kustomize import load_vars, switch_loaded_config_map, KubernetesManifest
from cpt.sizing import Sizing


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Search and replace variables in Kustomize k8s manifets.')
    parser.add_argument('--kustomize_builds_dir', type=str, required=True,
                        help='location of file produced by kustomize build')
    parser.add_argument('--kustomize_git_dir', type=str, required=True,
                        help='location of Kustomize git working dir with context dependent variables')
    parser.add_argument('--subfolder', type=str, required=True,
                        help='env specific subfolder in kustomize build directory')
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('-sc', help='switch kubectl context configuration', action='store_true')
    mutex_group.add_argument("-rv", help="replace variables", action='store_true')
    return parser


if __name__ == '__main__':
    parser = setup_arg_parser()
    args = parser.parse_args()

    builds_dir = args.kustomize_builds_dir
    subfolder = args.subfolder
    git_dir = args.kustomize_git_dir
    print(f"kustomize builds dir:{builds_dir}")
    print(f"kustomize builds subfolder:{subfolder}")
    print(f"kustomize_git_dir:{git_dir}")

    km = KubernetesManifest(builds_dir, git_dir, subfolder)
    sizing = Sizing(builds_dir, subfolder)
    if args.sc:
        # does not require other args - complicates redeploy_kust.sh
        switch_loaded_config_map(km.kustomize_git_dir)
    elif args.rv:
        # TODO vars_yaml Path contains TEST_ENV
        vars_yaml = Path(km.kustomize_git_dir, os.environ["TEST_ENV"] + '.yaml')
        vs = load_vars(vars_yaml)
        km.load_manifest(vs)
        sizing.save_sizing()
