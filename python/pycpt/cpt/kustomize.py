import re
from pathlib import Path
from typing import List

import yaml
from flatten_dict import flatten, unflatten

from cpt.common import debug_print, DEBUG_PRINT, error_print
from cpt.sizing import Sizing, containers


class KubernetesManifest(Sizing):
    """ manifest generated by Helm charts or Kustomize  loads generic manifest with placeholder for variables
        are replaced and output is written to interpolated_m which is used for actual deployment
    """

    def __init__(self, kustomize_builds_dir, kustomize_git_dir, subfolder, test_env: str,
                 generic_m='all_one20.yaml',
                 interpolated_m='all_one20_inter.yaml'):
        super().__init__(kustomize_builds_dir, subfolder, generic_m, interpolated_m)
        self.variable_placeholder_re = r"\$\(([\w]+)\)"
        # location of files with values of context dependent variables
        self.kustomize_git_dir = kustomize_git_dir
        self.variables: dict = {}
        # yaml file with env definition
        self.env_def = f"{test_env}.yaml"

    def interpolate_image(self, vars, image):
        try:
            ret = image
            placeholders = re.findall(self.variable_placeholder_re, ret)
            for placeholder in placeholders:
                debug_print(f"{image} has placeholders {placeholders}", DEBUG_PRINT)
                value = vars[placeholder]
                ret = re.sub(self.variable_placeholder_re, value, ret, 1)
            debug_print(f"{image}={ret}", DEBUG_PRINT)
        except KeyError as e:
            error_print(e, message=f"No {image} in test environment")
            ret = None
        return ret

    def load_manifest(self):
        containers_tuple = ('spec', 'template', 'spec', 'containers')
        init_containers_tuple = ('spec', 'template', 'spec', 'initContainers')
        debug_print(f"Loading manifest {self.generic_yaml.absolute()}", DEBUG_PRINT)
        with open(self.generic_yaml, 'r') as stream:
            try:
                docs: List = list(yaml.safe_load_all(stream))
                cont_docs = containers(docs)
                for i in range(0, len(docs)):
                    doc = docs[i]
                    if doc is not None and doc in cont_docs:
                        debug_print("Processing doc kind : {}".format(doc["kind"]), DEBUG_PRINT)
                        name = None
                        try:
                            doc_flat = flatten(doc)
                            for c in doc_flat[containers_tuple]:
                                name = c['name']
                                image = c["image"]
                                image_inter = self.interpolate_image(self.variables, image)
                                c['image'] = image_inter
                            try:
                                i_c = doc_flat[init_containers_tuple]
                                for c in i_c:
                                    image = c['image']
                                    image_inter = self.interpolate_image(self.variables, image)
                                    c['image'] = image_inter
                            except KeyError as e:
                                error_print(e, f"initContainers not present for {name}")
                            doc = unflatten(doc_flat)
                            with open(Path(self.kustomize_builds_dir, name + '_inter.yaml'), 'w') as outfile:
                                yaml.dump(doc, outfile, default_flow_style=False)
                        except KeyError as e:
                            error_print(e, f"image is empty dict")
                    docs[i] = doc
                with open(self.interpolated_yaml, 'w') as outfile:
                    debug_print(f"Writing {self.interpolated_yaml.resolve()}", DEBUG_PRINT)
                    yaml.dump_all(docs, outfile, default_flow_style=False)
            except yaml.YAMLError as e:
                error_print(e)

    def switch_loaded_config_map(self):
        """reads and let active only test env config map and saves the yaml back"""
        kust_yaml = Path(self.kustomize_git_dir, 'kustomization.yaml')
        new_doc = []
        with open(kust_yaml, 'r') as r_stream:
            try:
                docs = list(yaml.safe_load_all(r_stream))
                resources = docs[0]['resources'] if len(docs) == 1 else None
                debug_print(f"env def : {self.env_def}", DEBUG_PRINT)
                if resources is not None:
                    resources.append(self.env_def)
                    new_doc = docs[0]
            except yaml.YAMLError as e:
                error_print(e)

        with open(kust_yaml, 'w') as w_stream:
            try:
                yaml.dump(new_doc, w_stream)
            except yaml.YAMLError as e:
                error_print(e)

    def load_vars(self):
        vars_yaml = Path(self.kustomize_git_dir, self.env_def)
        debug_print(f"Loading variables from {vars_yaml.absolute()}", DEBUG_PRINT)
        with open(vars_yaml, 'r') as stream:
            try:
                docs = yaml.load_all(stream, Loader=yaml.FullLoader)
                for doc in docs:
                    try:
                        data_dict = doc["data"]
                        self.variables.update(data_dict)
                    except KeyError as e:
                        error_print(e)
                    continue
            except yaml.YAMLError as e:
                error_print(e)