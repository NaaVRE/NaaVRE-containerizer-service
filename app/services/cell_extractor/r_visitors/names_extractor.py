from app.services.cell_extractor.parseR.RParser import RParser
from app.services.cell_extractor.r_visitors.r_visitor import RVisitor


class NamesExtractor(RVisitor):
    # Get all names and try to infer their types.
    def __init__(self):
        self.names = {}
        self.scoped = set()

    def visitProg(self, ctx: RParser.ProgContext):
        self.visitChildren(ctx)
        return self.names

    def visitCall(self, ctx: RParser.CallContext):
        if isinstance(ctx.expr(), RParser.AssignContext):
            self.visit(ctx.expr())
        self.visit(ctx.sublist())

    def visitFor(self, ctx: RParser.ForContext):
        # Iterator variable is scoped
        self.scoped.add(ctx.ID().getText())
        # If what we iterate over is a variable, type should be list.
        if isinstance(ctx.expr(0), RParser.IdContext):
            self.visit(ctx.expr(0))
            id = ctx.expr(0).getText()
            self.names[id]['type'] = 'list'
        self.visit(ctx.expr(1))
        self.scoped.remove(ctx.ID().getText())

    def visitSub(self, ctx: RParser.SubContext):
        if isinstance(ctx.expr(), RParser.IdContext):
            self.visit(ctx.expr())

    def visitSublist(self, ctx: RParser.SublistContext):
        self.visitChildren(ctx)

    def visitAssign(self, ctx: RParser.AssignContext):
        # Get the identifier and the assigned value of the expr and add to dict
        id = self.visit(ctx.expr(0))
        xp1 = ctx.expr(1).getText()
        if id is None:
            return None

        if id in self.names and self.names[id]['type'] is not None:
            return None
        # Check if the value is an ID or an expression of which we can get type
        if xp1 == 'list':
            self.names[id] = {'name': id, 'type': 'list'}
        elif isinstance(ctx.expr(1), RParser.IdContext):
            self.names[id] = {'name': id, 'type': None}
        else:
            type = self.visit(ctx.expr(1))
            self.names[id] = {'name': id, 'type': type}

    def visitAddsub(self, ctx: RParser.AddsubContext):
        # Visit left and right expressions
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        # Check if left and right are in dict i.e. they're variables
        if left in self.names:
            left = self.names[left]
        if right in self.names:
            right = self.names[right]

        # Check if the left and right children are of the same type
        if left == "int" and right == "int":
            return "int"
        elif left == "float" or right == "float":
            return "float"
        else:
            return None

    def visitMuldiv(self, ctx: RParser.MuldivContext):
        # Same procedure as addsub
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if left in self.names:
            left = self.names[left]
        if right in self.names:
            right = self.names[right]
        if left == "int" and right == "int":
            return "int"
        elif left == "float" or right == "float":
            return "float"
        else:
            return None

    def visitId(self, ctx: RParser.IdContext):
        id = ctx.ID().getText()
        # Check if id is in dict, otherwise add it.
        if id not in self.names and id not in self.scoped:
            self.names[id] = {'name': id, 'type': None}
        return id

    def visitInt(self, ctx: RParser.IntContext):
        return "int"

    def visitFloat(self, ctx: RParser.FloatContext):
        return "float"

    def visitString(self, ctx: RParser.StringContext):
        return "str"
