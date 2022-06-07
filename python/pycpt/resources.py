import argparse
import os

from cpt.common import debug_print, DEBUG_PRINT
from cpt.kustomize import KubernetesManifest


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
    debug_print(f"kustomize builds dir:{builds_dir}", DEBUG_PRINT)
    debug_print(f"kustomize builds subfolder:{subfolder}", DEBUG_PRINT)
    debug_print(f"kustomize_git_dir:{git_dir}", DEBUG_PRINT)

    km = KubernetesManifest(builds_dir, git_dir, subfolder, test_env=os.getenv("TEST_ENV"))
    if args.sc:
        # does not require other args - complicates redeploy_kust.sh
        km.switch_loaded_config_map()
    elif args.rv:
        km.load_vars()
        km.load_manifest()
        km.save_sizing()
