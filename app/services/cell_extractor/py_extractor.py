import ast
import logging
import re
from functools import lru_cache

from pyflakes import reporter as pyflakes_reporter, api as pyflakes_api
from pytype import config as pytype_config
from pytype.tools.annotate_ast import annotate_ast

from .extractor import Extractor
from .py_conf_assignment_transformer import PyConfAssignmentTransformer
from .py_visitors.visitor import Visitor
from ...models.notebook_data import NotebookData


class PyExtractor(Extractor):
    sources: list
    imports: list
    configurations: list
    global_params: list
    global_secrets: list
    undefined: list

    def __init__(self, notebook_data: NotebookData):
        super().__init__(notebook_data)
        notebook = notebook_data.notebook
        # If cell_type is code and not starting with '!'
        self.sources = [nbcell.source for nbcell in notebook.cells
                        if nbcell.cell_type == 'code' and
                        len(nbcell.source) > 0 and
                        nbcell.source[0] != '!']
        self.visitor = self.__parse_code(
            '\n'.join(self.sources),
            infer_types=True,
        )
        self.imports = self.visitor.imports
        self.configurations = self.__extract_prefixed_var('conf')
        self.global_params = self.__extract_prefixed_var('param')
        self.global_secrets = self.__extract_prefixed_var('secret')
        for source in self.sources:
            self.undefined.append(self.__extract_cell_undefined(source))
        self.inputs = self.infer_cell_inputs()
        self.outputs = self.infer_cell_outputs()
        self.params = self.extract_cell_params()
        self.secrets = self.extract_cell_secrets()
        self.confs = self.extract_cell_conf_ref()
        self.dependencies = self.infer_cell_dependencies()

    def __extract_prefixed_var(self, prefix):
        extracted_vars = []
        for variable_name in self.visitor.variable_info:
            if variable_name.startswith(prefix + '_'):
                extracted_vars.append(
                    self.visitor.variable_info[variable_name])
        return extracted_vars

    def infer_cell_outputs(self):
        cell_names = self.__parse_code(self.source)
        outputs = []
        for var_name, properties in cell_names.items():
            if (var_name not in self.imports and
                    var_name not in self.undefined and
                    var_name not in self.configurations and
                    var_name not in self.global_params and
                    var_name not in self.global_secrets):
                outputs.append(properties)
        return outputs

    def infer_cell_inputs(self):
        cell_undefined = self.__extract_cell_undefined(self.source)
        inputs = []
        for var_name, properties in cell_undefined.items():
            if (var_name not in self.imports and
                    var_name not in self.configurations and
                    var_name not in self.global_params and
                    var_name not in self.global_secrets):
                inputs.append(properties)
        return inputs

    def infer_cell_dependencies(self):
        dependencies = []
        names = self.__parse_code(self.source)

        for ck in self.confs:
            names.update(self.__parse_code(self.confs[ck]))

        for name in names:
            if name in self.imports:
                dependencies.append(self.imports.get(name))

        return dependencies

    def infer_cell_conf_dependencies(self, confs):
        dependencies = []
        for ck in confs:
            for name in self.__parse_code(confs[ck]):
                if name in self.imports:
                    dependencies.append(self.imports.get(name))

        return dependencies

    @staticmethod
    @lru_cache
    def __get_annotated_ast(cell_source):
        return annotate_ast.annotate_source(
            cell_source, ast, pytype_config.Options.create())

    def __convert_type_annotation(self, type_annotation):
        """ Convert type annotation to the ones supported for cell interfaces

        :param type_annotation: type annotation obtained by e.g. pytype
        :return: converted type: 'int', 'float', 'str', 'list', or None
        """
        if type_annotation is None:
            return None

        patterns = {
            'int': [
                re.compile(r'^int$'),
            ],
            'float': [
                re.compile(r'^float$'),
            ],
            'str': [
                re.compile(r'^str$'),
            ],
            'list': [
                re.compile(r'^List\['),
            ],
            None: [
                re.compile(r'^Any$'),
                re.compile(r'^Dict'),
                re.compile(r'^Callable'),
            ]
        }
        for type_name, regs in patterns.items():
            for reg in regs:
                if reg.match(type_annotation):
                    return type_name

        logging.getLogger(__name__).debug(f'Unmatched type: {type_annotation}')
        return None

    def __parse_code(self, source_code, infer_types=False):
        if infer_types:
            tree = self.__get_annotated_ast(source_code)
        else:
            tree = ast.parse(source_code)
        visitor = Visitor()
        visitor.visit(tree)
        return visitor

    def __extract_cell_undefined(self, cell_source):
        flakes_stdout = StreamList()
        flakes_stderr = StreamList()
        rep = pyflakes_reporter.Reporter(
            flakes_stdout.reset(),
            flakes_stderr.reset())
        pyflakes_api.check(cell_source, filename="temp", reporter=rep)
        if rep._stderr():
            raise SyntaxError("Flakes reported the following error:"
                              "\n{}".format('\t' + '\t'.join(rep._stderr())))
        p = r"'(.+?)'"
        out = rep._stdout()
        undef_vars = dict()
        for line in filter(lambda a: a != '\n' and 'undefined name' in a, out):
            var_search = re.search(p, line)
            var_name = var_search.group(1)
            undef_vars[var_name] = {
                'name': var_name,
                'type': self.visitor.variable_info[var_name]['type']
            }
        return undef_vars

    def extract_cell_params(self):
        params = []
        cell_unds = self.__extract_cell_undefined(self.source)
        param_unds = [und for und in cell_unds if und in self.global_params]
        for u in param_unds:
            if u not in params:
                params[u] = self.global_params[u]
        return params

    def extract_cell_secrets(self):
        secrets = []
        cell_unds = self.__extract_cell_undefined(self.source)
        secret_unds = [und for und in cell_unds if und in self.global_secrets]
        for u in secret_unds:
            if u not in secrets:
                secrets[u] = self.global_secrets[u]
        return secrets

    def extract_cell_conf_ref(self):
        confs = {}
        cell_unds = self.__extract_cell_undefined(self.source)
        conf_unds = [und for und in cell_unds if und in self.configurations]
        for u in conf_unds:
            if u not in confs:
                confs[u] = self.configurations[u]
        return []

    def __resolve_configurations(self, configurations):
        assignment_transformer = PyConfAssignmentTransformer(configurations)
        resolved_configurations = {
            k: ast.unparse(assignment_transformer.visit(ast.parse(v)))
            for k, v in configurations.items()
        }
        configurations.update(resolved_configurations)
        return configurations


class StreamList:

    def __init__(self):
        self.out = list()

    def write(self, text):
        self.out.append(text)

    def reset(self):
        self.out = list()
        return self

    def __call__(self):
        return self.out
