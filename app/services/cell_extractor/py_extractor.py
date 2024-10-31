import ast
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
        # self.undefined = []
        # for source in self.sources:
        #     self.undefined.append(self.__extract_cell_undefined(source))
        self.inputs = self.get_cell_inputs()
        self.outputs = self.get_cell_outputs()
        self.params = self.get_cell_params()
        self.secrets = self.get_cell_secrets()
        self.confs = self.extract_cell_conf_ref()
        self.dependencies = self.get_cell_dependencies()

    def __extract_prefixed_var(self, prefix):
        extracted_vars = []
        for variable_name in self.visitor.variable_info:
            if variable_name.startswith(prefix + '_'):
                extracted_vars.append(
                    self.visitor.variable_info[variable_name])
        return extracted_vars

    def is_var_name_in(self, var_name, dict_set):
        for frozen_dict in dict_set:
            dictionary = dict(frozen_dict)
            if var_name in dictionary:
                return True
        return False

    def get_cell_outputs(self):
        outputs = []
        cell_undefined = self.__extract_cell_undefined(self.source)
        for var_name, properties in self.visitor.variable_info.items():
            if var_name not in cell_undefined and \
                    not self.is_var_name_in(var_name, self.imports) and \
                    not self.is_var_name_in(var_name,
                                            self.configurations) and \
                    not self.is_var_name_in(var_name, self.global_params) and \
                    not self.is_var_name_in(var_name, self.global_secrets):
                outputs.append({'name': var_name,
                                'value': properties['value'],
                                'type': properties['type']})
        return outputs

    def get_cell_inputs(self):
        cell_undefined = self.__extract_cell_undefined(self.source)
        inputs = []
        for var_name, properties in cell_undefined.items():
            if (not self.is_var_name_in(var_name, self.imports) and
                    not self.is_var_name_in(var_name, self.configurations) and
                    not self.is_var_name_in(var_name, self.global_params) and
                    not self.is_var_name_in(var_name, self.global_secrets)):
                inputs.append({'name': var_name,
                               'value': properties['value'],
                               'type': properties['type']})
        return inputs

    def get_cell_dependencies(self):
        dependencies = []
        return dependencies

    def infer_cell_conf_dependencies(self, confs):
        pass

    @staticmethod
    @lru_cache
    def __get_annotated_ast(cell_source):
        return annotate_ast.annotate_source(
            cell_source, ast, pytype_config.Options.create())

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
        undef_vars = {}
        for line in filter(lambda a: a != '\n' and 'undefined name' in a, out):
            var_search = re.search(p, line)
            var_name = var_search.group(1)
            undef_vars[var_name] = (self.get_variable_info(var_name))
        return undef_vars

    def get_cell_params(self):
        params = []
        cell_unds = self.__extract_cell_undefined(self.source)
        param_unds = [und for und in cell_unds if und in self.global_params]
        for u in param_unds:
            if u not in params:
                params[u] = self.global_params[u]
        return params

    def get_cell_secrets(self):
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

    def get_variable_info(self, var_name):
        for var in self.visitor.variable_info:
            if var == var_name:
                return self.visitor.variable_info[var]


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
