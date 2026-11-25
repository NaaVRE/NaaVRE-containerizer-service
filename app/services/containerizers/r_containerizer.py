from abc import ABC

from app.models.workflow_cell import Cell
from app.services.containerizers.containerizer import Containerizer


class RContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell, module_mapping_url=None,
                 service_version=None, template_format_version=None):
        super().__init__(cell=cell, module_mapping_url=module_mapping_url,
                         service_version=service_version,
                         template_format_version=template_format_version)
        self.file_extension = '.R'
        self.template_script = 'R_cell_template.jinja2'

    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        def normalize_module_name(name):
            if name.lower().startswith('r-'):
                name = name[2:]
            return name.casefold()

        r_mapping = {
            normalize_module_name(name): mapped_name
            for name, mapped_name in module_name_mapping.get('r', {}).items()
        }
        conda_deps = set()
        for dependency in dependencies:
            name = dependency['name']
            normalized_name = normalize_module_name(name)
            if normalized_name in r_mapping:
                conda_deps.add(r_mapping[normalized_name])
            else:
                conda_deps.add('r-' + name)

        pip_deps = set()
        conda_deps.discard(None)
        return {'conda_dependencies': conda_deps, 'pip_dependencies': pip_deps}

    def build_script(self):
        template_script = self.template_env.get_template(self.template_script)
        deps = self.cell.dependencies
        conf = self.cell.confs
        r_dependencies = []
        for dep in deps:
            install_packages = ('if (!requireNamespace("' + dep['name'] +
                                '", quietly = TRUE)) {\n\tinstall.packages("' +
                                dep['name'] +
                                '", repos="http://cran.us.r-project.org")\n}')
            r_dependencies.append(install_packages)
            library = 'library(' + dep['name'] + ')'
            r_dependencies.append(library)
        return template_script.render(cell=self.cell,
                                      deps=r_dependencies,
                                      confs=conf)
