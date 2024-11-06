import ast
import logging
import re
from functools import lru_cache
from typing import Literal

from pyflakes import reporter as pyflakes_reporter, api as pyflakes_api
from pytype import config as pytype_config
from pytype.tools.annotate_ast import annotate_ast

from .extractor import Extractor
from .py_conf_assignment_transformer import PyConfAssignmentTransformer
from .py_visitors.visitor import Visitor
from ..repositories.github_service import logger
from ...models.notebook_data import NotebookData


class PyExtractor(Extractor):
    notebook_sources: list
    notebook_imports: dict
    notebook_configurations: dict
    notebook_params: dict
    # notebook_secrets: dict
    undefined: dict

    def __init__(self, notebook_data: NotebookData):
        # If cell_type is code and not starting with '!'
        notebook = notebook_data.notebook
        self.notebook_sources = [nbcell.source for nbcell in notebook.cells if
                                 nbcell.cell_type == 'code' and len(
                                     nbcell.source) > 0 and nbcell.source[
                                     0] != '!']
        self.notebook_variables = self.__extract_variables(
            '\n'.join(self.notebook_sources),
            infer_types=True,
        )
        notebook_visitor = (
            self.__parse_code('\n'.join(self.notebook_sources),
                              infer_types=True,
                              ))

        self.notebook_imports = self.__extract_imports(self.notebook_sources)

        visitor_imports = notebook_visitor.imports
        for imp in self.notebook_imports:
            if imp not in visitor_imports:
                print(f'Warning: {imp} not found in imports')

        self.notebook_configurations = self.__extract_configurations(
            self.notebook_sources)
        self.notebook_params = self.__extract_prefixed_var(
            self.notebook_sources, 'param')
        self.notebook_secrets = self.__extract_prefixed_var(
            self.notebook_sources,
            'secret')
        self.undefined = dict()
        for source in self.notebook_sources:
            self.undefined.update(self.__extract_cell_undefined(source))
        super().__init__(notebook_data)

    def __parse_code(self, source_code, infer_types=False):
        if infer_types:
            tree = self.__get_annotated_ast(source_code)
        else:
            tree = ast.parse(source_code)
        visitor = Visitor()
        visitor.visit(tree)
        return visitor

    def __extract_imports(self, sources):
        imports = {}
        for s in sources:
            tree = ast.parse(s)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom,)):
                    for n in node.names:
                        key = n.asname if n.asname else n.name
                        if key not in imports:
                            imports[key] = {
                                'name': n.name,
                                'asname': n.asname or None,
                                'module': node.module if isinstance(
                                    node, ast.ImportFrom) else ""
                            }
        return imports

    def __extract_configurations(self, sources):
        configurations = {}
        for s in sources:
            lines = s.splitlines()
            tree = ast.parse(s)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    target = node.targets[0]
                    if hasattr(target, 'id'):
                        name = node.targets[0].id
                        prefix = name.split('_')[0]
                        if prefix == 'conf' and name not in configurations:
                            conf_line = ''
                            for line in lines[node.lineno - 1:node.end_lineno]:
                                conf_line += line.strip()
                            configurations[name] = conf_line
        return self.__resolve_configurations(configurations)

    def __extract_prefixed_var(self, sources,
                               prefix:
                               Literal['input', 'output', 'param', 'secret']):
        extracted_vars = dict()
        for s in sources:
            lines = s.splitlines()
            tree = ast.parse(s)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and hasattr(node.targets[0],
                                                            'id'):
                    name = node.targets[0].id
                    node_prefix = name.split('_')[0]
                    if node_prefix == prefix:
                        var_line = ''
                        for line in lines[node.lineno - 1:node.end_lineno]:
                            var_line += line.strip()
                        var_value = ast.unparse(node.value)
                        try:
                            # remove quotes around strings
                            var_value = str(ast.literal_eval(var_value))
                            # Cast according to
                            # self.notebook_names[name]['type']
                            if self.notebook_variables[name]['type'] == 'int':
                                var_value = int(var_value)
                            elif (self.notebook_variables[name]['type']
                                  == 'float'):
                                var_value = float(var_value)
                            elif (self.notebook_variables[name]['type']
                                  == 'list'):
                                var_value = list(ast.literal_eval(var_value))
                            elif (self.notebook_variables[name]['type'] ==
                                  'str'):
                                var_value = str(var_value)
                        except ValueError:
                            # when var_value can't safely be parsed,
                            pass
                        extracted_vars[name] = {
                            'name': name,
                            'type': self.notebook_variables[name]['type'],
                            'value': var_value,
                        }
                        if prefix == 'secret':
                            del extracted_vars[name]['value']
        return extracted_vars

    def infer_cell_outputs(self) -> list[dict]:
        cell_variables = self.__extract_variables(self.cell_source)
        cell_outputs = []
        for name, properties in cell_variables.items():
            if (name not in self.__extract_cell_undefined(self.cell_source) and
                    name not in self.notebook_imports and
                    name in self.undefined and
                    name not in self.notebook_configurations and
                    name not in self.notebook_params and
                    name not in self.notebook_secrets):
                cell_outputs.append({'name': name, 'type': properties['type']})
        # outs = {
        #     name: properties
        #     for name, properties in cell_variables.items()
        #     if name not in self.__extract_cell_undefined(self.cell_source)
        #        and name not in self.notebook_imports
        #        and name in self.undefined
        #        and name not in self.notebook_configurations
        #        and name not in self.notebook_params
        #        and name not in self.notebook_secrets
        # }
        return cell_outputs

    def infer_cell_inputs(self) -> list[dict]:
        cell_undefined = self.__extract_cell_undefined(self.cell_source)
        cell_inputs = []
        for und, properties in cell_undefined.items():
            if (und not in self.notebook_imports and
                    und not in self.notebook_configurations and
                    und not in self.notebook_params and
                    und not in self.notebook_secrets):
                cell_inputs.append({'name': und, 'type': properties['type']})
        return cell_inputs

    def infer_cell_dependencies(self, confs):
        dependencies = []
        names = self.__extract_variables(self.cell_source)
        for ck in confs:
            conf_vars = self.__extract_variables(ck['assignation'])
            names.update(conf_vars)
        for name in names:
            if name in self.notebook_imports:
                dependencies.append(self.notebook_imports.get(name))
        return dependencies

    def infer_cell_conf_dependencies(self, confs):
        dependencies = []
        for ck in confs:
            for name in self.__extract_variables(confs[ck]):
                if name in self.notebook_imports:
                    dependencies.append(self.notebook_imports.get(name))

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

    def __extract_variables(self, cell_source, infer_types=False):
        names = dict()
        if infer_types:
            tree = self.__get_annotated_ast(cell_source)
        else:
            tree = ast.parse(cell_source)
        for module in ast.walk(tree):
            if isinstance(module, (ast.Name,)):
                var_name = module.id
                if infer_types:
                    try:
                        var_type = self.__convert_type_annotation(
                            module.resolved_annotation)
                    except AttributeError:
                        logger.debug(
                            '__extract_variables failed. var_name: %s', )
                        var_type = None
                else:
                    var_type = self.notebook_variables[var_name]['type']
                names[module.id] = {
                    'name': var_name,
                    'type': var_type,
                }
        return names

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
                'type': self.notebook_variables[var_name]['type'],
            }
        return undef_vars

    def extract_cell_params(self) -> list[dict]:
        param = {}
        cell_params = []
        cell_unds = self.__extract_cell_undefined(self.cell_source)
        param_unds = [und for und in cell_unds if und in self.notebook_params]
        for u in param_unds:
            if u not in param:
                param[u] = self.notebook_params[u]
                cell_params.append({'name': u, 'type': param[u]['type'],
                                    'default_value': param[u]['value']})
        return cell_params

    def extract_cell_secrets(self) -> list[dict]:
        secret = {}
        cell_secret = []
        cell_unds = self.__extract_cell_undefined(self.cell_source)
        secret_unds = [und for und in cell_unds if
                       und in self.notebook_secrets]
        for u in secret_unds:
            if u not in secret:
                secret[u] = self.notebook_secrets[u]
                cell_secret.append(secret)
        return cell_secret

    def extract_cell_conf_ref(self) -> list[dict]:
        conf = {}
        cell_confs = []
        cell_unds = self.__extract_cell_undefined(self.cell_source)
        conf_unds = [und for und in cell_unds if
                     und in self.notebook_configurations]
        for u in conf_unds:
            if u not in conf:
                conf[u] = self.notebook_configurations[u]
                cell_confs.append({'name': u, 'assignation': conf[u]})
        return cell_confs

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
