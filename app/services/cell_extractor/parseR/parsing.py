from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream

from app.services.cell_extractor.parseR.RFilter import RFilter
from app.services.cell_extractor.parseR.RLexer import RLexer
from app.services.cell_extractor.parseR.RParser import RParser


def parse_text(text):
    input_stream = InputStream(text)
    lexer = RLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    r_filter = RFilter(tokens)
    r_filter.stream()
    tokens.reset()

    parser = RParser(tokens)
    tree = parser.prog()

    return tree
