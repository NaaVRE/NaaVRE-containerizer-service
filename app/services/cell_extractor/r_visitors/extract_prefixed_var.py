import json

from app.services.cell_extractor.parseR.RParser import RParser
from app.services.cell_extractor.r_visitors.r_visitor import RVisitor


class ExtractPrefixedVar(RVisitor):
    def __init__(self, prefix):
        self.prefix = prefix + '_'
        self.params = {}

    def visitProg(self, ctx: RParser.ProgContext):
        self.visitChildren(ctx)
        return self.params

    def visitAssign(self, ctx: RParser.AssignContext):
        # Get the identifier and the assigned value of the expr and add to dict
        var_id = self.visit(ctx.expr(0))
        if var_id is None:
            return None
        # check if id has param_ prefix
        if var_id.startswith(self.prefix):  # and id not in self.params:
            if (self.params[var_id]['value'] is None or var_id not in
                    self.params):
                expr = self.visit(ctx.expr(1))
                # If returned expression is empty e.g. in case of unaccessible
                # env variables, do not specify type.
                if expr != "":
                    self.params[var_id] = {'value': expr,
                                           'type': type(expr).__name__}
                else:
                    self.params[var_id] = {'value': expr, 'type': None}
        return None

    def visitCall(self, ctx: RParser.CallContext):

        if isinstance(ctx.expr(), RParser.AssignContext):
            if ctx.expr().expr(1).getText() == 'list':
                # convert string to list
                list_val = ctx.sublist().getText()
                try:
                    val = json.loads('[' + list_val + ']')
                except json.JSONDecodeError:
                    val = None
                self.params[ctx.expr().expr(0).getText()] = {'value': val,
                                                             'type': 'list'}

    def visitId(self, ctx: RParser.IdContext):
        var_id = ctx.ID().getText()
        if var_id.startswith(self.prefix) and var_id not in self.params:
            self.params[var_id] = {'value': None, 'type': None}

        return str(var_id)

    def visitInt(self, ctx: RParser.IntContext):
        val = ctx.INT().getText()
        # check if L suffix is present
        if val[-1] == "L":
            val = val[:-1]
        return int(val)

    def visitFloat(self, ctx: RParser.FloatContext):
        val = ctx.FLOAT().getText()
        return float(val)

    def visitString(self, ctx: RParser.StringContext):
        val = ctx.STRING().getText()
        return str(val[1:-1])
