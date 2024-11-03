from app.services.cell_extractor.parseR.RParser import RParser
from app.services.cell_extractor.r_visitors.r_visitor import RVisitor


built_in = ["T", "F", "pi", "is.numeric", "mu", "round"]


class ExtractUndefined(RVisitor):
    def __init__(self, defs, scoped):
        self.undefined = set()
        self.defs = defs
        self.scoped = scoped

    def visitProg(self, ctx: RParser.ProgContext):
        self.visitChildren(ctx)
        return self.undefined

    def visitAssign(self, ctx: RParser.AssignContext):
        self.visitChildren(ctx)

    def visitCall(self, ctx: RParser.CallContext):
        # If expr startswith 'function', all sub variables are scoped.
        if ctx.expr().getText().startswith('function'):
            for sub in ctx.sublist().sub():
                self.scoped.add(sub.getText())
        else:
            if isinstance(ctx.expr(), RParser.UseropContext):
                self.visit(ctx.expr())
            self.visit(ctx.sublist())

    # TEST
    def visitUserop(self, ctx: RParser.UseropContext):
        if isinstance(ctx.expr(0), RParser.CallContext):
            self.visit(ctx.expr(0))
        if isinstance(ctx.expr(1), RParser.CallContext):
            self.visit(ctx.expr(1))

    def visitSublist(self, ctx: RParser.SublistContext):
        self.visitChildren(ctx)

    def visitExtract(self, ctx: RParser.ExtractContext):
        self.visit(ctx.expr(0))

    def visitSub(self, ctx: RParser.SubContext):
        if isinstance(ctx.expr(), RParser.IdContext):
            self.visit(ctx.expr())
        elif isinstance(ctx.expr(), RParser.AssignContext):
            self.scoped.add(ctx.expr().expr(0).getText())
            self.visit(ctx.expr().expr(1))
        elif isinstance(ctx.expr(), RParser.CallContext):
            self.visit(ctx.expr())
        elif isinstance(ctx.expr(), RParser.FunctionContext):
            self.visit(ctx.expr())

    def visitFunction(self, ctx: RParser.FunctionContext):
        self.visit(ctx.formlist())
        self.visit(ctx.expr())

    def visitFormlist(self, ctx: RParser.FormlistContext):
        self.visitChildren(ctx)

    def visitForm(self, ctx: RParser.FormContext):
        self.scoped.add(ctx.ID().getText())
        if isinstance(ctx.expr(), RParser.IdContext):
            self.visit(ctx.expr())

    def visitFor(self, ctx: RParser.ForContext):
        # Iterator variable is scoped
        self.scoped.add(ctx.ID().getText())
        self.visit(ctx.expr(0))
        self.visit(ctx.expr(1))
        self.scoped.remove(ctx.ID().getText())

    def visitId(self, ctx: RParser.IdContext):
        id = ctx.ID().getText()
        if (id not in self.defs and id not in self.scoped and id
                not in built_in):
            self.undefined.add(ctx.getText())
