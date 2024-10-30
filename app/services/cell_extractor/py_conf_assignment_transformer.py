import ast


class PyConfAssignmentTransformer(ast.NodeTransformer):

    def __init__(self, configurations):
        # get the 'value' side of configuration assignments
        self.conf_values = {
            k: ast.parse(v).body[0].value
            for k, v in configurations.items()
        }

    def visit_Assign(self, node):
        # visit the 'value' side of assignments (*<node.targets> = node.value)
        node.value = self.generic_visit(node.value)
        return node

    def visit_Name(self, node):
        # replace variable names starting with 'conf_' by their value
        if not node.id.startswith('conf_'):
            return node
        if node.id not in self.conf_values:
            raise ValueError(f'{node.id} is not defined')
        # Recursively call self.visit() to replace names in dropped-in values
        return self.visit(self.conf_values[node.id])
