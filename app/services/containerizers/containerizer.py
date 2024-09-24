import json
import os
from abc import abstractmethod
from pathlib import Path

import requests
from jinja2 import Environment, PackageLoader

from app.models.cell import Cell


def load_module_name_mapping():
    module_mapping_url = os.getenv('MODULE_MAPPING_URL','https://raw.githubusercontent.com/QCDIS/NaaVRE-conf/main/module_mapping.json')
    module_mapping = {}
    if module_mapping_url:
        resp = requests.get(module_mapping_url)
        module_mapping = json.loads(resp.text)
    module_name_mapping_path = os.path.join(
        str(Path.home()), 'NaaVRE', 'module_name_mapping.json')
    if not os.path.exists(module_name_mapping_path):
        with open(module_name_mapping_path, 'w') as module_name_mapping_file:
            json.dump(module_mapping, module_name_mapping_file, indent=4)
        module_name_mapping_file.close()

    module_name_mapping_file = open(module_name_mapping_path)
    loaded_module_name_mapping = json.load(module_name_mapping_file)
    loaded_module_name_mapping.update(module_mapping)
    module_name_mapping_file.close()
    return loaded_module_name_mapping


class Containerizer():

    def __init__(self,cell: Cell):
        self.cell = cell
        self.check_has_type()
        self.check_has_base_image()
        loader = PackageLoader('app', 'templates')
        self.template_env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        self.visualization_cell = False
        if self.cell.title.lower().startswith('visualize-'):
            self.visualization_cell = True


    def check_has_type(self):
        all_vars = self.cell.params + self.cell.inputs + self.cell.outputs
        for parm_name in all_vars:
            if parm_name not in self.cell.types:
                raise ValueError(parm_name + ' has not type')
        pass

    def check_has_base_image(self):
        if self.cell.base_image is None:
            raise ValueError('base_image is not set')
        pass



    @abstractmethod
    def build_cell(self):
        pass

    @abstractmethod
    def extract_notebook(self):
        pass

    def build_environment(self):
        template_conda = self.template_env.get_template('conda_env_template.jinja2')
        mapped_dependencies = self.map_dependencies(dependencies=self.cell.dependencies,
                                                    module_name_mapping=load_module_name_mapping())
        return template_conda.render(base_image=self.cell.base_image, conda_deps=list(
            mapped_dependencies['conda_dependencies']), pip_deps=list(mapped_dependencies['pip_dependencies']))

    @abstractmethod
    def is_standard_module(self, module_name):
        pass

    def build_docker(self):
        template_dockerfile = self.template_env.get_template('dockerfile_template_conda.jinja2')
        return template_dockerfile.render(task_name=self.cell.task_name, base_image=self.cell.base_image)

    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        set_conda_deps = set([])
        set_pip_deps = set([])
        for dep in dependencies:
            module_name = None
            if 'module' in dep and dep['module']:
                if '.' in dep['module']:
                    module_name = dep['module'].split('.')[0]
                else:
                    module_name = dep['module']
            elif 'name' in dep and dep['name']:
                module_name = dep['name']
            if module_name:
                conda_package = True
                pip_package = False
                if module_name in module_name_mapping['conda'].keys():
                    module_name = module_name_mapping['conda'][module_name]
                    pip_package = False
                    conda_package = True
                if module_name in module_name_mapping['pip'].keys():
                    module_name = module_name_mapping['pip'][module_name]
                    pip_package = True
                    conda_package = False
                if module_name is None:
                    continue
                if not self.is_standard_module(module_name):
                    if conda_package:
                        set_conda_deps.add(module_name)
                    if pip_package:
                        set_pip_deps.add(module_name)
        return {'conda_dependencies': set_conda_deps, 'pip_dependencies': set_pip_deps}

