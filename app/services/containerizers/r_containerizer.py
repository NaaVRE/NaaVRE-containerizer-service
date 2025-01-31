from abc import ABC

from app.models.workflow_cell import Cell
from app.services.containerizers.containerizer import Containerizer


class RContainerizer(Containerizer, ABC):

    def __init__(self, cell: Cell):
        super().__init__(cell)
        self.file_extension = '.R'
        self.template_script = 'R_cell_template.jinja2'

    def build_visualization_template_cell(self):
        raise NotImplementedError

    def map_dependencies(self, dependencies=None, module_name_mapping=None):
        dependencies = map(
            lambda x: 'r-' + x['name'],
            dependencies)
        dependencies = map(
            lambda x: module_name_mapping.get('r', {}).get(x, x),
            dependencies)
        conda_deps = set(dependencies)
        pip_deps = set()
        conda_deps.discard(None)
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
