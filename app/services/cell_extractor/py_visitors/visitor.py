import ast


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = {}
        self.variable_info = {}
        self.variables = []
        self.function_info = set()

    # Get all the variable reads
    def visit_Name(self, node):
        var_name = node.id
        if (var_name not in self.variable_info and
                var_name not in self.function_info):
            self.variable_info[var_name] = {
                'type': 'unknown',
                'value': None
            }
            self.variables.append({'name': var_name,
                                   'type': 'unknown',
                                   'value': None})
        self.generic_visit(node)

    # Get all the function calls
    def visit_Call(self, node):
        self.function_info.add(self.get_full_name(node.func))
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Check if there's a target and it's a Name (variable)
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            var_value = None
            var_type = 'unknown'

            # Try to infer type and value from the assigned expression
            # Handles constants (str, int, float, bool)
            if isinstance(node.value,
                          ast.Constant):
                var_value = node.value.value
                var_type = type(var_value).__name__
            elif isinstance(node.value, ast.List):
                var_value = [
                    elt.value if isinstance(elt, ast.Constant) else '...'
                    for elt in node.value.elts]
                var_type = 'list'
            elif isinstance(node.value, ast.Dict):
                var_value = {key.value if isinstance(key,
                                                     ast.Constant) else
                             '...': val.value if isinstance(
                    val, ast.Constant) else '...' for key, val in
                             zip(node.value.keys, node.value.values)}
                var_type = 'dict'
            elif isinstance(node.value, ast.Set):
                var_value = {
                    elt.value if isinstance(elt, ast.Constant) else '...'
                    for elt in node.value.elts}
                var_type = 'set'
            elif isinstance(node.value, ast.Tuple):
                var_value = tuple(
                    elt.value if isinstance(elt, ast.Constant) else '...'
                    for elt in node.value.elts)
                var_type = 'tuple'
            elif isinstance(node.value, ast.BinOp):
                # determine if type is int or float
                var_type = 'int' if isinstance(node.value.op, ast.BitXor) \
                    else 'float'
            # If variable name starts with 'secret_', hide the value
            if var_name.startswith("secret_"):
                var_value = None
            # Store in dictionary
            self.variable_info[var_name] = {
                'type': var_type,
                'value': var_value
            }
            self.variables.append({'name': var_name,
                                   'type': var_type,
                                   'value': var_value})
        self.generic_visit(node)

    def visit_Import(self, node):
        # For regular imports (e.g., import os)
        for alias in node.names:
            code_import = {alias.name: {'module': '', 'asname': alias.asname}}
            self.imports.update(code_import)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # For relative imports (e.g., from os import path)
        module = node.module if node.module else ""
        for alias in node.names:
            code_import = {alias.name: {'asname': alias.asname,
                                        'module': module}}
            self.imports.update(code_import)
        self.generic_visit(node)

    def get_full_name(self, node):
        # Recursively get the full name for nodes of type `ast.Attribute`
        if isinstance(node, ast.Name):  # Base case for the recursion
            return node.id
        elif isinstance(node, ast.Attribute):  # Recursive case
            return f"{self.get_full_name(node.value)}.{node.attr}"
        return None
