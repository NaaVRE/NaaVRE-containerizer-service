import os
from abc import abstractmethod

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

    @abstractmethod
    def build_script(self):
        template_script = self.template_env.get_template(self.template_script)
        deps = self.cell.dependencies
        conf = self.cell.confs

        return template_script.render(cell=self.cell,
                                      deps=deps,
                                      confs=conf)

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
            title=self.cell.title,
            base_image=self.cell.base_container_image)

    @abstractmethod
    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        pass

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
