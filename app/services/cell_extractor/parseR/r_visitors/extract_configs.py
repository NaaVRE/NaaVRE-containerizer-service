from app.services.cell_extractor.parseR.RParser import RParser
from app.services.cell_extractor.parseR.r_visitors.r_visitor import RVisitor


class ExtractConfigs(RVisitor):
    def __init__(self):
        self.configs = {}

    def visitProg(self, ctx: RParser.ProgContext):
        self.visitChildren(ctx)
        return self.configs

    def visitAssign(self, ctx: RParser.AssignContext):
        # Get the identifier and the assigned value of the expr and add to dict
        id = self.visit(ctx.expr(0))

        if id is None:
            return None

        # check if id has conf_ prefix
        if id.startswith("conf_") and id not in self.configs:
            self.configs[id] = ctx.getText()

        return None

    def visitId(self, ctx: RParser.IdContext):
        return ctx.ID().getText()

    def visitString(self, ctx: RParser.StringContext):
        # In the case of environment variables, identifier could be string.
        return ctx.STRING().getText()
