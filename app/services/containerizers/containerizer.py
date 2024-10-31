import os
from abc import abstractmethod

import autopep8
import requests
from jinja2 import Environment, PackageLoader

from app.models.workflow_cell import Cell


def get_module_name_mapping():
    module_mapping_url = os.getenv('MODULE_MAPPING_URL',
                                   'https://raw.githubusercontent.com/QCDIS'
                                   '/NaaVRE-conf/main/module_mapping.json')
    try:
        return requests.get(module_mapping_url).json()
    except Exception as e:
        raise ValueError('Failed to load module mapping from ' +
                         module_mapping_url) from e


class Containerizer():

    def __init__(self, cell: Cell):
        self.cell = cell
        self.cell.clean_code()
        self.cell.clean_title()
        self.cell.clean_task_name()
        self.check_has_type()
        self.check_has_base_image()
        loader = PackageLoader('app', 'templates')
        self.template_env = Environment(loader=loader, trim_blocks=True,
                                        lstrip_blocks=True)
        self.visualization_cell = False
        if self.cell.title.lower().startswith('visualize-'):
            self.visualization_cell = True
        self.file_extension = ''
        self.template_script = ''
        self.template_conda_env = 'conda_env_template.jinja2'
        self.dockerfile_template = 'dockerfile_template_conda.jinja2'

    def check_has_type(self):
        all_vars = self.cell.params + self.cell.inputs + self.cell.outputs
        for param_name in all_vars:
            if param_name not in self.cell.types:
                raise ValueError(param_name + ' has not type')
        pass

    def check_has_base_image(self):
        if self.cell.base_container_image is None:
            raise ValueError('base_image is not set')
        pass

    @abstractmethod
    def build_script(self):
        template_script = self.template_env.get_template(self.template_script)
        deps = self.cell.generate_dependencies()
        types = self.cell.types
        conf = self.cell.generate_configuration_dict()
        self.cell.container_source = autopep8.fix_code(
            template_script.render(cell=self.cell,
                                   deps=deps,
                                   types=types,
                                   confs=conf))
        return template_script.render(cell=self.cell,
                                      deps=self.cell.generate_dependencies(),
                                      types=self.cell.types,
                                      confs=self.cell.
                                      generate_configuration_dict())

    @abstractmethod
    def extract_notebook(self):
        pass

    def build_environment(self):
        template_conda = self.template_env.get_template(
            self.template_conda_env)
        mapped_dependencies = self.map_dependencies(
            dependencies=self.cell.dependencies,
            module_name_mapping=get_module_name_mapping())
        return template_conda.render(base_image=self.cell.base_container_image,
                                     conda_deps=list(
                                         mapped_dependencies[
                                             'conda_dependencies']),
                                     pip_deps=list(mapped_dependencies[
                                                       'pip_dependencies']))

    @abstractmethod
    def is_standard_module(self, module_name):
        pass

    def build_docker(self):
        template_dockerfile = self.template_env.get_template(
            self.dockerfile_template)
        return template_dockerfile.render(
                task_name=self.cell.task_name,
                base_image=self.cell.base_container_image)

    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        conda_deps = set()
        pip_deps = set()
        for dep in dependencies:
            module_name = dep.get('module', dep.get('name'))
            if not module_name:
                continue
            module_name = module_name.split('.')[
                0] if '.' in module_name else module_name
            if module_name in module_name_mapping['conda']:
                conda_deps.add(module_name_mapping['conda'][module_name])
            elif module_name in module_name_mapping['pip']:
                pip_deps.add(module_name_mapping['pip'][module_name])
            elif not self.is_standard_module(module_name):
                conda_deps.add(module_name)
        return {'conda_dependencies': conda_deps, 'pip_dependencies': pip_deps}

    # def map_dependencies(self, dependencies=None, module_name_mapping=None):
    #     set_conda_deps = set([])
    #     set_pip_deps = set([])
    #     for dep in dependencies:
    #         module_name = None
    #         if 'module' in dep and dep['module']:
    #             if '.' in dep['module']:
    #                 module_name = dep['module'].split('.')[0]
    #             else:
    #                 module_name = dep['module']
    #         elif 'name' in dep and dep['name']:
    #             module_name = dep['name']
    #         if module_name:
    #             conda_package = True
    #             pip_package = False
    #             if module_name in module_name_mapping['conda'].keys():
    #                 module_name = module_name_mapping['conda'][module_name]
    #                 pip_package = False
    #                 conda_package = True
    #             if module_name in module_name_mapping['pip'].keys():
    #                 module_name = module_name_mapping['pip'][module_name]
    #                 pip_package = True
    #                 conda_package = False
    #             if module_name is None:
    #                 continue
    #             if not self.is_standard_module(module_name):
    #                 if conda_package:
    #                     set_conda_deps.add(module_name)
    #                 if pip_package:
    #                     set_pip_deps.add(module_name)
    #     return {'conda_dependencies': set_conda_deps,
    #             'pip_dependencies': set_pip_deps}
