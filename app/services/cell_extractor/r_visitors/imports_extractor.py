from app.services.cell_extractor.parseR.RParser import RParser
from app.services.cell_extractor.r_visitors.r_visitor import RVisitor


class ImportsExtractor(RVisitor):
    def __init__(self):
        self.imports = {}

    def visitProg(self, ctx: RParser.ProgContext):
        self.visitChildren(ctx)
        return self.imports

    def visitCall(self, ctx: RParser.CallContext):
        # Check function call of library or require functions indicating an
        # import.
        fun = self.visit(ctx.expr())
        if fun == "library" or fun == "require":
            lib = self.visit(ctx.sublist()).strip('"')
            self.imports[lib] = lib

    def visitId(self, ctx: RParser.IdContext):
        return ctx.ID().getText()

    def visitString(self, ctx: RParser.StringContext):
        return ctx.STRING().getText()
