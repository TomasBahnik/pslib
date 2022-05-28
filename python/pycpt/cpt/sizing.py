import json
from pathlib import Path
from typing import List

import pandas as pd
import yaml
from jinja2 import Template

from cpt.constants import RESOURCE_RE, units_conversion


class Sizing:
    def __init__(self, kustomize_builds_dir, subfolder, generic_m='all_one20.yaml',
                 interpolated_m='all_one20_inter.yaml'):
        # location of file produced by kustomize build
        self.kustomize_builds_dir = kustomize_builds_dir
        self.subfolder = subfolder
        self.generic_m = generic_m
        self.interpolated = interpolated_m
        self.subfolder_path = Path(kustomize_builds_dir, subfolder)
        self.interpolated_yaml = Path(self.subfolder_path, interpolated_m)
        self.generic_yaml = Path(self.subfolder_path, generic_m)

    def save_sizing(self, base_file_name='sizing'):
        dir_path = self.subfolder_path
        input_yaml = self.interpolated_yaml
        output_json = Path(dir_path, base_file_name + '.json')
        output_html = Path(dir_path, base_file_name + '.html')
        output_csv = Path(dir_path, base_file_name + '.csv')
        metrics = extract_resources(input_yaml)
        volumes = extract_volumes(input_yaml)
        metrics.update({'volumes': volumes})
        print(f"Create sizing from {input_yaml} to {output_json}")
        with open(output_json, "w") as json_file:
            json.dump(metrics, json_file, indent=4, sort_keys=True)
        # remove key for html/csv
        metrics.pop('volumes', None)
        html = template_html.render(module_resources=sorted(metrics.items(), key=lambda item: item[0]))
        with open(output_html, "w") as html_file:
            html_file.write(html)
        n_m = normalize_metrics(metrics)  # overwrites original. Use deep copy if problem
        csv = template_csv.render(module_resources=sorted(n_m.items(), key=lambda item: item[0]))
        with open(output_csv, "w") as csv_file:
            csv_file.write(csv)
        return metrics


# spec.volumeClaimTemplates[0].spec.resources.requests.storage
def extract_volumes(file):
    resources_dict = {}
    with open(file, 'r') as stream:
        try:
            docs = yaml.load_all(stream, Loader=yaml.FullLoader)
            for doc in docs:
                if doc is not None:
                    resources = None
                    storage = None
                    print("Processing doc kind : {}".format(doc["kind"]))
                    try:
                        volumes = doc["spec"]["volumeClaimTemplates"][0]["spec"]["resources"]["requests"]
                        service_name = doc["spec"]["serviceName"]
                    except KeyError as e:
                        print("volumeClaimTemplates can't be read from doc kind : {}".format(doc["kind"]))
                        continue
                    try:
                        resources = volumes["storage"]
                        resources_dict[service_name] = resources
                    except KeyError as e:
                        print("name : {}, resources : {} KeyError {}".format(storage, resources, e))
        except yaml.YAMLError as exc:
            print(exc)
        return resources_dict


# TODO add spec.template.spec.initContainers[2].image - no resources but just version
# e.g image: atapaasregistry.azurecr.io/rolling/known-properties-docker:20210712110914
# which need to be changed when moving to new version
# helm template . > helm_sizing.yaml in YAML_TEMPLATES_DIR


template_html = Template('''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    </head>
    <body>
    <h2>Resources</h2>
    <table border="1" cellpadding="5">
        <tr><th>module</th><th colspan="2">limits</th><th colspan="2">requests</th></tr>
        <tr><th></th><th>memory</th><th>cpu</th><th>memory</th><th>cpu</th><th>replicas</th><th>image</th></tr>
        {% for module, resources in module_resources %}
        <tr>
            <td>{{module}}</td>
            <td>{{resources['limits']['memory']}}</td><td>{{resources['limits']['cpu']}}</td>
            <td>{{resources['requests']['memory']}}</td><td>{{resources['requests']['cpu']}}</td><td>{{resources['replicas']}}</td><td>{{resources['image']}}</td>
        </tr>            
        {% endfor %}
    </table>
    </body>
    </html> 
    ''')
template_csv = Template('''module,memory_limits,cpu_limits,memory_requests,cpu_requests,replicas
{% for module, resources in module_resources %}{{module}},{{resources['limits']['memory']}},{{resources['limits']['cpu']}},{{resources['requests']['memory']}},{{resources['requests']['cpu']}},{{resources['replicas']}}
{% endfor %}
''')


def get_resources(resources, key, sub_key):
    if key in resources and sub_key in resources[key]:
        return resources[key][sub_key]
    else:
        return None


# original metrics are replaces by floats - use for csv
def normalize_metrics(metrics):
    for module, resources in metrics.items():
        l_mem = get_resources(resources, 'limits', 'memory')
        l_cpu = get_resources(resources, 'limits', 'cpu')
        r_mem = get_resources(resources, 'requests', 'memory')
        r_cpu = get_resources(resources, 'requests', 'cpu')
        print("get resource values for module {}".format(module))
        metrics[module]['limits']['memory'] = resource_value(l_mem)
        metrics[module]['limits']['cpu'] = resource_value(l_cpu)
        metrics[module]['requests']['memory'] = resource_value(r_mem)
        metrics[module]['requests']['cpu'] = resource_value(r_cpu)
    return metrics


def resource_value(str_value):
    if not str_value or str_value is None:
        return None
    match = RESOURCE_RE.match(str_value)
    # only value
    if match.lastindex == 1:
        v = float(match.group(1))
        return v
    # both value and units
    if match.lastindex > 1:
        v = float(match.group(1))
        u = RESOURCE_RE.match(str_value).group(2)
        # missing unit => no change
        f = float(units_conversion[u]) if u else 1
        return v * f
    else:
        return None


def compare_resources(r1, r2):
    df1 = pd.read_csv(r1)
    df2 = pd.read_csv(r2)
    return pd.merge(df1, df2, on=['module'], how='outer', suffixes=('_helm', '_kust'))


def extract_resources(file):
    resources_dict = {}
    with open(file, 'r') as stream:
        try:
            docs = yaml.load_all(stream, Loader=yaml.FullLoader)
            cont_docs = containers(docs)
            for doc in cont_docs:
                if doc is not None:
                    resources = None
                    name = None
                    image = None
                    # only doc kind = Deployment has resources etc.
                    print("Processing doc kind : {}".format(doc["kind"]))
                    container = doc["spec"]["template"]["spec"]["containers"][0]
                    try:
                        name = container["name"]
                    except KeyError as e:
                        print("name : {}, resources : {} KeyError {}".format(name, resources, e))
                    try:
                        resources = container["resources"]
                    except KeyError as e:
                        print("name : {}, resources set to empty dict, KeyError {}".format(name, e))
                        resources = {}  # empty is not None
                    try:
                        image = container["image"]
                    except KeyError as e:
                        print("name : {}, image set to empty dict, KeyError {}".format(name, e))
                        resources = {}  # empty is not None
                    try:
                        replicas = doc["spec"]["replicas"]
                    except KeyError as e:
                        print("name : {}, replicas set to None, KeyError {}".format(name, e))
                        replicas = None
                if name is not None and resources is not None:
                    if resources:
                        print("Add non empty resources {} = {}".format(name, resources))
                        resources.update({'replicas': replicas})
                        resources.update({'image': image})
                        resources_dict[name] = resources
                    else:
                        # can't explicitly access keys limits and requests - leads to unclear html template
                        print("Add empty resources for {}".format(name))
                        resources_dict[name] = {'limits': {}, 'requests': {}, 'replicas': {}}
        except yaml.YAMLError as exc:
            print(exc)
        return resources_dict


def containers(docs):
    d_c: List[dict] = []
    for doc in docs:
        try:
            # test existence of the keys
            test = doc["spec"]["template"]["spec"]["containers"]
            d_c.append(doc)
            print("containers found in : {}".format(doc["kind"]))
        except KeyError as e:
            # print("containers can't be read from doc kind : {}".format(doc["kind"]))
            continue
    return d_c
