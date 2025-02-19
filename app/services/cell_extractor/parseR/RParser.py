# Generated from R.g4 by ANTLR 4.13.1
# encoding: utf-8
import sys

import antlr4
from antlr4 import ParserRuleContext
from antlr4.BufferedTokenStream import TokenStream
from antlr4.Parser import Parser
from antlr4.PredictionContext import PredictionContextCache
from antlr4.RuleContext import RuleContext
from antlr4.atn.ATN import ATN
from antlr4.atn.ATNDeserializer import ATNDeserializer
from antlr4.atn.ParserATNSimulator import ParserATNSimulator
from antlr4.dfa.DFA import DFA
from antlr4.error.Errors import RecognitionException, NoViableAltException
from antlr4.tree.Tree import ParseTreeListener, ParseTreeVisitor

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 64, 216, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7,
        4, 2, 5, 7, 5, 2, 6, 7,
        6, 1, 0, 1, 0, 5, 0, 17, 8, 0, 10, 0, 12, 0, 20, 9, 0, 1, 0, 5, 0, 23,
        8, 0, 10, 0, 12, 0, 26,
        9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 3, 1, 40, 8, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 99, 8, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 5, 1,
        153, 8, 1, 10, 1, 12, 1, 156, 9, 1, 1, 2, 1, 2, 1, 2, 3, 2, 161, 8, 2,
        5, 2, 163, 8, 2, 10,
        2, 12, 2, 166, 9, 2, 1, 2, 3, 2, 169, 8, 2, 1, 3, 1, 3, 1, 3, 5, 3,
        174, 8, 3, 10, 3, 12, 3,
        177, 9, 3, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 3, 4, 185, 8, 4, 1, 5,
        1, 5, 1, 5, 5, 5, 190,
        8, 5, 10, 5, 12, 5, 193, 9, 5, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1,
        6, 1, 6, 1, 6, 1, 6, 1,
        6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 3, 6, 214, 8, 6, 1,
        6, 0, 1, 2, 7, 0, 2, 4,
        6, 8, 10, 12, 0, 9, 2, 0, 1, 1, 63, 63, 1, 0, 10, 11, 1, 0, 5, 6, 1, 0,
        7, 8, 1, 0, 13, 14,
        1, 0, 15, 20, 1, 0, 22, 23, 1, 0, 24, 25, 1, 0, 27, 32, 270, 0, 24, 1,
        0, 0, 0, 2, 98, 1,
        0, 0, 0, 4, 168, 1, 0, 0, 0, 6, 170, 1, 0, 0, 0, 8, 184, 1, 0, 0, 0,
        10, 186, 1, 0, 0, 0, 12,
        213, 1, 0, 0, 0, 14, 18, 3, 2, 1, 0, 15, 17, 7, 0, 0, 0, 16, 15, 1, 0,
        0, 0, 17, 20, 1, 0,
        0, 0, 18, 16, 1, 0, 0, 0, 18, 19, 1, 0, 0, 0, 19, 23, 1, 0, 0, 0, 20,
        18, 1, 0, 0, 0, 21, 23,
        5, 63, 0, 0, 22, 14, 1, 0, 0, 0, 22, 21, 1, 0, 0, 0, 23, 26, 1, 0, 0,
        0, 24, 22, 1, 0, 0, 0,
        24, 25, 1, 0, 0, 0, 25, 27, 1, 0, 0, 0, 26, 24, 1, 0, 0, 0, 27, 28, 5,
        0, 0, 1, 28, 1, 1, 0,
        0, 0, 29, 30, 6, 1, -1, 0, 30, 31, 7, 1, 0, 0, 31, 99, 3, 2, 1, 37, 32,
        33, 5, 21, 0, 0, 33,
        99, 3, 2, 1, 31, 34, 35, 5, 26, 0, 0, 35, 99, 3, 2, 1, 28, 36, 37, 5,
        33, 0, 0, 37, 39, 5,
        34, 0, 0, 38, 40, 3, 6, 3, 0, 39, 38, 1, 0, 0, 0, 39, 40, 1, 0, 0, 0,
        40, 41, 1, 0, 0, 0, 41,
        42, 5, 35, 0, 0, 42, 99, 3, 2, 1, 25, 43, 44, 5, 36, 0, 0, 44, 45, 3,
        4, 2, 0, 45, 46, 5,
        37, 0, 0, 46, 99, 1, 0, 0, 0, 47, 48, 5, 38, 0, 0, 48, 49, 5, 34, 0, 0,
        49, 50, 3, 2, 1, 0,
        50, 51, 5, 35, 0, 0, 51, 52, 3, 2, 1, 22, 52, 99, 1, 0, 0, 0, 53, 54,
        5, 38, 0, 0, 54, 55,
        5, 34, 0, 0, 55, 56, 3, 2, 1, 0, 56, 57, 5, 35, 0, 0, 57, 58, 3, 2, 1,
        0, 58, 59, 5, 39, 0,
        0, 59, 60, 3, 2, 1, 21, 60, 99, 1, 0, 0, 0, 61, 62, 5, 40, 0, 0, 62,
        63, 5, 34, 0, 0, 63,
        64, 5, 61, 0, 0, 64, 65, 5, 41, 0, 0, 65, 66, 3, 2, 1, 0, 66, 67, 5,
        35, 0, 0, 67, 68, 3,
        2, 1, 20, 68, 99, 1, 0, 0, 0, 69, 70, 5, 42, 0, 0, 70, 71, 5, 34, 0, 0,
        71, 72, 3, 2, 1, 0,
        72, 73, 5, 35, 0, 0, 73, 74, 3, 2, 1, 19, 74, 99, 1, 0, 0, 0, 75, 76,
        5, 43, 0, 0, 76, 99,
        3, 2, 1, 18, 77, 78, 5, 44, 0, 0, 78, 99, 3, 2, 1, 17, 79, 99, 5, 45,
        0, 0, 80, 99, 5, 46,
        0, 0, 81, 82, 5, 34, 0, 0, 82, 83, 3, 2, 1, 0, 83, 84, 5, 35, 0, 0, 84,
        99, 1, 0, 0, 0, 85,
        99, 5, 61, 0, 0, 86, 99, 5, 60, 0, 0, 87, 99, 5, 56, 0, 0, 88, 99, 5,
        57, 0, 0, 89, 99, 5,
        58, 0, 0, 90, 99, 5, 59, 0, 0, 91, 99, 5, 47, 0, 0, 92, 99, 5, 48, 0,
        0, 93, 99, 5, 49, 0,
        0, 94, 99, 5, 50, 0, 0, 95, 99, 5, 51, 0, 0, 96, 99, 5, 52, 0, 0, 97,
        99, 5, 53, 0, 0, 98,
        29, 1, 0, 0, 0, 98, 32, 1, 0, 0, 0, 98, 34, 1, 0, 0, 0, 98, 36, 1, 0,
        0, 0, 98, 43, 1, 0, 0,
        0, 98, 47, 1, 0, 0, 0, 98, 53, 1, 0, 0, 0, 98, 61, 1, 0, 0, 0, 98, 69,
        1, 0, 0, 0, 98, 75,
        1, 0, 0, 0, 98, 77, 1, 0, 0, 0, 98, 79, 1, 0, 0, 0, 98, 80, 1, 0, 0, 0,
        98, 81, 1, 0, 0, 0,
        98, 85, 1, 0, 0, 0, 98, 86, 1, 0, 0, 0, 98, 87, 1, 0, 0, 0, 98, 88, 1,
        0, 0, 0, 98, 89, 1,
        0, 0, 0, 98, 90, 1, 0, 0, 0, 98, 91, 1, 0, 0, 0, 98, 92, 1, 0, 0, 0,
        98, 93, 1, 0, 0, 0, 98,
        94, 1, 0, 0, 0, 98, 95, 1, 0, 0, 0, 98, 96, 1, 0, 0, 0, 98, 97, 1, 0,
        0, 0, 99, 154, 1, 0,
        0, 0, 100, 101, 10, 40, 0, 0, 101, 102, 7, 2, 0, 0, 102, 153, 3, 2, 1,
        41, 103, 104, 10,
        39, 0, 0, 104, 105, 7, 3, 0, 0, 105, 153, 3, 2, 1, 40, 106, 107, 10,
        38, 0, 0, 107, 108,
        5, 9, 0, 0, 108, 153, 3, 2, 1, 38, 109, 110, 10, 36, 0, 0, 110, 111, 5,
        12, 0, 0, 111,
        153, 3, 2, 1, 37, 112, 113, 10, 35, 0, 0, 113, 114, 5, 62, 0, 0, 114,
        153, 3, 2, 1, 36,
        115, 116, 10, 34, 0, 0, 116, 117, 7, 4, 0, 0, 117, 153, 3, 2, 1, 35,
        118, 119, 10, 33,
        0, 0, 119, 120, 7, 1, 0, 0, 120, 153, 3, 2, 1, 34, 121, 122, 10, 32, 0,
        0, 122, 123, 7,
        5, 0, 0, 123, 153, 3, 2, 1, 33, 124, 125, 10, 30, 0, 0, 125, 126, 7, 6,
        0, 0, 126, 153,
        3, 2, 1, 31, 127, 128, 10, 29, 0, 0, 128, 129, 7, 7, 0, 0, 129, 153, 3,
        2, 1, 30, 130,
        131, 10, 27, 0, 0, 131, 132, 5, 26, 0, 0, 132, 153, 3, 2, 1, 28, 133,
        134, 10, 26, 0,
        0, 134, 135, 7, 8, 0, 0, 135, 153, 3, 2, 1, 27, 136, 137, 10, 42, 0, 0,
        137, 138, 5, 2,
        0, 0, 138, 139, 3, 10, 5, 0, 139, 140, 5, 3, 0, 0, 140, 141, 5, 3, 0,
        0, 141, 153, 1, 0,
        0, 0, 142, 143, 10, 41, 0, 0, 143, 144, 5, 4, 0, 0, 144, 145, 3, 10, 5,
        0, 145, 146, 5,
        3, 0, 0, 146, 153, 1, 0, 0, 0, 147, 148, 10, 24, 0, 0, 148, 149, 5, 34,
        0, 0, 149, 150,
        3, 10, 5, 0, 150, 151, 5, 35, 0, 0, 151, 153, 1, 0, 0, 0, 152, 100, 1,
        0, 0, 0, 152, 103,
        1, 0, 0, 0, 152, 106, 1, 0, 0, 0, 152, 109, 1, 0, 0, 0, 152, 112, 1, 0,
        0, 0, 152, 115,
        1, 0, 0, 0, 152, 118, 1, 0, 0, 0, 152, 121, 1, 0, 0, 0, 152, 124, 1, 0,
        0, 0, 152, 127,
        1, 0, 0, 0, 152, 130, 1, 0, 0, 0, 152, 133, 1, 0, 0, 0, 152, 136, 1, 0,
        0, 0, 152, 142,
        1, 0, 0, 0, 152, 147, 1, 0, 0, 0, 153, 156, 1, 0, 0, 0, 154, 152, 1, 0,
        0, 0, 154, 155,
        1, 0, 0, 0, 155, 3, 1, 0, 0, 0, 156, 154, 1, 0, 0, 0, 157, 164, 3, 2,
        1, 0, 158, 160, 7,
        0, 0, 0, 159, 161, 3, 2, 1, 0, 160, 159, 1, 0, 0, 0, 160, 161, 1, 0, 0,
        0, 161, 163, 1,
        0, 0, 0, 162, 158, 1, 0, 0, 0, 163, 166, 1, 0, 0, 0, 164, 162, 1, 0, 0,
        0, 164, 165, 1,
        0, 0, 0, 165, 169, 1, 0, 0, 0, 166, 164, 1, 0, 0, 0, 167, 169, 1, 0, 0,
        0, 168, 157, 1,
        0, 0, 0, 168, 167, 1, 0, 0, 0, 169, 5, 1, 0, 0, 0, 170, 175, 3, 8, 4,
        0, 171, 172, 5, 54,
        0, 0, 172, 174, 3, 8, 4, 0, 173, 171, 1, 0, 0, 0, 174, 177, 1, 0, 0, 0,
        175, 173, 1, 0,
        0, 0, 175, 176, 1, 0, 0, 0, 176, 7, 1, 0, 0, 0, 177, 175, 1, 0, 0, 0,
        178, 185, 5, 61, 0,
        0, 179, 180, 5, 61, 0, 0, 180, 181, 5, 29, 0, 0, 181, 185, 3, 2, 1, 0,
        182, 185, 5, 55,
        0, 0, 183, 185, 5, 53, 0, 0, 184, 178, 1, 0, 0, 0, 184, 179, 1, 0, 0,
        0, 184, 182, 1, 0,
        0, 0, 184, 183, 1, 0, 0, 0, 185, 9, 1, 0, 0, 0, 186, 191, 3, 12, 6, 0,
        187, 188, 5, 54,
        0, 0, 188, 190, 3, 12, 6, 0, 189, 187, 1, 0, 0, 0, 190, 193, 1, 0, 0,
        0, 191, 189, 1, 0,
        0, 0, 191, 192, 1, 0, 0, 0, 192, 11, 1, 0, 0, 0, 193, 191, 1, 0, 0, 0,
        194, 214, 3, 2, 1,
        0, 195, 196, 5, 61, 0, 0, 196, 214, 5, 29, 0, 0, 197, 198, 5, 61, 0, 0,
        198, 199, 5, 29,
        0, 0, 199, 214, 3, 2, 1, 0, 200, 201, 5, 60, 0, 0, 201, 214, 5, 29, 0,
        0, 202, 203, 5,
        60, 0, 0, 203, 204, 5, 29, 0, 0, 204, 214, 3, 2, 1, 0, 205, 206, 5, 47,
        0, 0, 206, 214,
        5, 29, 0, 0, 207, 208, 5, 47, 0, 0, 208, 209, 5, 29, 0, 0, 209, 214, 3,
        2, 1, 0, 210, 214,
        5, 55, 0, 0, 211, 214, 5, 53, 0, 0, 212, 214, 1, 0, 0, 0, 213, 194, 1,
        0, 0, 0, 213, 195,
        1, 0, 0, 0, 213, 197, 1, 0, 0, 0, 213, 200, 1, 0, 0, 0, 213, 202, 1, 0,
        0, 0, 213, 205,
        1, 0, 0, 0, 213, 207, 1, 0, 0, 0, 213, 210, 1, 0, 0, 0, 213, 211, 1, 0,
        0, 0, 213, 212,
        1, 0, 0, 0, 214, 13, 1, 0, 0, 0, 14, 18, 22, 24, 39, 98, 152, 154, 160,
        164, 168, 175,
        184, 191, 213
    ]


class RParser(Parser):
    grammarFileName = "R.g4"
    atn = ATNDeserializer().deserialize(serializedATN())
    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]
    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "';'", "'[['", "']'", "'['", "'::'", "':::'",
                    "'$'", "'@'", "'^'", "'-'", "'+'", "':'", "'*'", "'/'",
                    "'>'", "'>='", "'<'", "'<='", "'=='", "'!='", "'!'",
                    "'&'", "'&&'", "'|'", "'||'", "'~'", "'<-'", "'<<-'",
                    "'='", "'->'", "'->>'", "':='", "'function'", "'('",
                    "')'", "'{'", "'}'", "'if'", "'else'", "'for'", "'in'",
                    "'while'", "'repeat'", "'?'", "'next'", "'break'",
                    "'NULL'", "'NA'", "'Inf'", "'NaN'", "'TRUE'", "'FALSE'",
                    "'.'", "','", "'...'"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "HEX", "INT", "FLOAT", "COMPLEX", "STRING", "ID",
                     "USER_OP", "NL", "WS"]

    RULE_prog = 0
    RULE_expr = 1
    RULE_exprlist = 2
    RULE_formlist = 3
    RULE_form = 4
    RULE_sublist = 5
    RULE_sub = 6

    ruleNames = ["prog", "expr", "exprlist", "formlist", "form", "sublist",
                 "sub"]

    EOF = antlr4.Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    T__53 = 54
    T__54 = 55
    HEX = 56
    INT = 57
    FLOAT = 58
    COMPLEX = 59
    STRING = 60
    ID = 61
    USER_OP = 62
    NL = 63
    WS = 64

    def __init__(self, input_token: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input_token, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA,
                                          self.sharedContextCache)
        self._predicates = None

    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invoking_state: int = -1):
            super().__init__(parent, invoking_state)
            self.parser = parser

        def EOF(self):
            return self.getToken(RParser.EOF, 0)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def NL(self, i: int = None):
            if i is None:
                return self.getTokens(RParser.NL)
            else:
                return self.getToken(RParser.NL, i)

        def getRuleIndex(self):
            return RParser.RULE_prog

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterProg"):
                listener.enterProg(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitProg"):
                listener.exitProg(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitProg"):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)

    def prog(self):
        localctx = RParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and (
                    (1 << _la) & -4665732143054320640) != 0):
                self.state = 22
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10, 11, 21, 26, 33, 34, 36, 38, 40, 42, 43, 44,
                             45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 57, 58,
                             59, 60, 61]:
                    self.state = 14
                    self.expr(0)
                    self.state = 18
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 0,
                                                        self._ctx)
                    while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            self.state = 15
                            _la = self._input.LA(1)
                            if not (_la == 1 or _la == 63):
                                self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 20
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input, 0,
                                                            self._ctx)

                    pass
                elif token in [63]:
                    self.state = 21
                    self.match(RParser.NL)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 26
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 27
            self.match(RParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = - 1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return RParser.RULE_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class NextContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNext"):
                listener.enterNext(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNext"):
                listener.exitNext(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNext"):
                return visitor.visitNext(self)
            else:
                return visitor.visitChildren(self)

    class ParensContext(ExprContext):
        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterParens"):
                listener.enterParens(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitParens"):
                listener.exitParens(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParens"):
                return visitor.visitParens(self)
            else:
                return visitor.visitChildren(self)

    class CompareContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCompare"):
                listener.enterCompare(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCompare"):
                listener.exitCompare(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCompare"):
                return visitor.visitCompare(self)
            else:
                return visitor.visitChildren(self)

    class StringContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(RParser.STRING, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterString"):
                listener.enterString(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitString"):
                listener.exitString(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitString"):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)

    class UseropContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def USER_OP(self):
            return self.getToken(RParser.USER_OP, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterUserop"):
                listener.enterUserop(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitUserop"):
                listener.exitUserop(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitUserop"):
                return visitor.visitUserop(self)
            else:
                return visitor.visitChildren(self)

    class ForContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(RParser.ID, 0)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFor"):
                listener.enterFor(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFor"):
                listener.exitFor(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFor"):
                return visitor.visitFor(self)
            else:
                return visitor.visitChildren(self)

    class DotContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterDot"):
                listener.enterDot(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitDot"):
                listener.exitDot(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDot"):
                return visitor.visitDot(self)
            else:
                return visitor.visitChildren(self)

    class AddsubContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAddsub"):
                listener.enterAddsub(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAddsub"):
                listener.exitAddsub(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAddsub"):
                return visitor.visitAddsub(self)
            else:
                return visitor.visitChildren(self)

    class Index2Context(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def sublist(self):
            return self.getTypedRuleContext(RParser.SublistContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIndex2"):
                listener.enterIndex2(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIndex2"):
                listener.exitIndex2(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIndex2"):
                return visitor.visitIndex2(self)
            else:
                return visitor.visitChildren(self)

    class UnaryContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterUnary"):
                listener.enterUnary(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitUnary"):
                listener.exitUnary(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitUnary"):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)

    class WhileContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterWhile"):
                listener.enterWhile(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitWhile"):
                listener.exitWhile(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitWhile"):
                return visitor.visitWhile(self)
            else:
                return visitor.visitChildren(self)

    class FloatContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(RParser.FLOAT, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFloat"):
                listener.enterFloat(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFloat"):
                listener.exitFloat(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFloat"):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)

    class NotContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNot"):
                listener.enterNot(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNot"):
                listener.exitNot(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNot"):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)

    class AndContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAnd"):
                listener.enterAnd(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAnd"):
                listener.exitAnd(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAnd"):
                return visitor.visitAnd(self)
            else:
                return visitor.visitChildren(self)

    class FunctionContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def formlist(self):
            return self.getTypedRuleContext(RParser.FormlistContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFunction"):
                listener.enterFunction(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFunction"):
                listener.exitFunction(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFunction"):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)

    class RepeatContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterRepeat"):
                listener.enterRepeat(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitRepeat"):
                listener.exitRepeat(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRepeat"):
                return visitor.visitRepeat(self)
            else:
                return visitor.visitChildren(self)

    class ComplexContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def COMPLEX(self):
            return self.getToken(RParser.COMPLEX, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterComplex"):
                listener.enterComplex(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitComplex"):
                listener.exitComplex(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitComplex"):
                return visitor.visitComplex(self)
            else:
                return visitor.visitChildren(self)

    class BlockContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def exprlist(self):
            return self.getTypedRuleContext(RParser.ExprlistContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBlock"):
                listener.enterBlock(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBlock"):
                listener.exitBlock(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlock"):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)

    class HexContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def HEX(self):
            return self.getToken(RParser.HEX, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterHex"):
                listener.enterHex(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitHex"):
                listener.exitHex(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitHex"):
                return visitor.visitHex(self)
            else:
                return visitor.visitChildren(self)

    class NanContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNan"):
                listener.enterNan(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNan"):
                listener.exitNan(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNan"):
                return visitor.visitNan(self)
            else:
                return visitor.visitChildren(self)

    class IdContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(RParser.ID, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterId"):
                listener.enterId(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitId"):
                listener.exitId(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitId"):
                return visitor.visitId(self)
            else:
                return visitor.visitChildren(self)

    class PowerContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPower"):
                listener.enterPower(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPower"):
                listener.exitPower(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPower"):
                return visitor.visitPower(self)
            else:
                return visitor.visitChildren(self)

    class IfContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIf"):
                listener.enterIf(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIf"):
                listener.exitIf(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIf"):
                return visitor.visitIf(self)
            else:
                return visitor.visitChildren(self)

    class SeqContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSeq"):
                listener.enterSeq(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSeq"):
                listener.exitSeq(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSeq"):
                return visitor.visitSeq(self)
            else:
                return visitor.visitChildren(self)

    class InfContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterInf"):
                listener.enterInf(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitInf"):
                listener.exitInf(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitInf"):
                return visitor.visitInf(self)
            else:
                return visitor.visitChildren(self)

    class OrContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterOr"):
                listener.enterOr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitOr"):
                listener.exitOr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOr"):
                return visitor.visitOr(self)
            else:
                return visitor.visitChildren(self)

    class BreakContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBreak"):
                listener.enterBreak(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBreak"):
                listener.exitBreak(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBreak"):
                return visitor.visitBreak(self)
            else:
                return visitor.visitChildren(self)

    class FalseContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFalse"):
                listener.enterFalse(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFalse"):
                listener.exitFalse(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFalse"):
                return visitor.visitFalse(self)
            else:
                return visitor.visitChildren(self)

    class IndexContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def sublist(self):
            return self.getTypedRuleContext(RParser.SublistContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIndex"):
                listener.enterIndex(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIndex"):
                listener.exitIndex(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIndex"):
                return visitor.visitIndex(self)
            else:
                return visitor.visitChildren(self)

    class IntContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(RParser.INT, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterInt"):
                listener.enterInt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitInt"):
                listener.exitInt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitInt"):
                return visitor.visitInt(self)
            else:
                return visitor.visitChildren(self)

    class MuldivContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMuldiv"):
                listener.enterMuldiv(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMuldiv"):
                listener.exitMuldiv(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMuldiv"):
                return visitor.visitMuldiv(self)
            else:
                return visitor.visitChildren(self)

    class IfelseContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIfelse"):
                listener.enterIfelse(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIfelse"):
                listener.exitIfelse(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIfelse"):
                return visitor.visitIfelse(self)
            else:
                return visitor.visitChildren(self)

    class CallContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def sublist(self):
            return self.getTypedRuleContext(RParser.SublistContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCall"):
                listener.enterCall(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCall"):
                listener.exitCall(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCall"):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)

    class HelpContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterHelp"):
                listener.enterHelp(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitHelp"):
                listener.exitHelp(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitHelp"):
                return visitor.visitHelp(self)
            else:
                return visitor.visitChildren(self)

    class NaContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNa"):
                listener.enterNa(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNa"):
                listener.exitNa(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNa"):
                return visitor.visitNa(self)
            else:
                return visitor.visitChildren(self)

    class ExtractContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterExtract"):
                listener.enterExtract(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitExtract"):
                listener.exitExtract(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExtract"):
                return visitor.visitExtract(self)
            else:
                return visitor.visitChildren(self)

    class NullContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNull"):
                listener.enterNull(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNull"):
                listener.exitNull(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNull"):
                return visitor.visitNull(self)
            else:
                return visitor.visitChildren(self)

    class UtildeContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterUtilde"):
                listener.enterUtilde(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitUtilde"):
                listener.exitUtilde(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitUtilde"):
                return visitor.visitUtilde(self)
            else:
                return visitor.visitChildren(self)

    class TrueContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTrue"):
                listener.enterTrue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTrue"):
                listener.exitTrue(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTrue"):
                return visitor.visitTrue(self)
            else:
                return visitor.visitChildren(self)

    class NamespaceContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNamespace"):
                listener.enterNamespace(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNamespace"):
                listener.exitNamespace(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNamespace"):
                return visitor.visitNamespace(self)
            else:
                return visitor.visitChildren(self)

    class BtildeContext(ExprContext):

        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBtilde"):
                listener.enterBtilde(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBtilde"):
                listener.exitBtilde(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBtilde"):
                return visitor.visitBtilde(self)
            else:
                return visitor.visitChildren(self)

    class AssignContext(ExprContext):
        def __init__(self, parser,
                     ctx: ParserRuleContext):  # actually a RParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAssign"):
                listener.enterAssign(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAssign"):
                listener.exitAssign(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAssign"):
                return visitor.visitAssign(self)
            else:
                return visitor.visitChildren(self)

    def expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RParser.ExprContext(self, self._ctx, _parentState)
        # _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 4,
                                               self._ctx)
            if la_ == 1:
                localctx = RParser.UnaryContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx

                self.state = 30
                _la = self._input.LA(1)
                if not (_la == 10 or _la == 11):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 31
                self.expr(37)
                pass

            elif la_ == 2:
                localctx = RParser.NotContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 32
                self.match(RParser.T__20)
                self.state = 33
                self.expr(31)
                pass

            elif la_ == 3:
                localctx = RParser.UtildeContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 34
                self.match(RParser.T__25)
                self.state = 35
                self.expr(28)
                pass

            elif la_ == 4:
                localctx = RParser.FunctionContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 36
                self.match(RParser.T__32)
                self.state = 37
                self.match(RParser.T__33)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and (
                        (1 << _la) & 2350879005487398912) != 0):
                    self.state = 38
                    self.formlist()

                self.state = 41
                self.match(RParser.T__34)
                self.state = 42
                self.expr(25)
                pass

            elif la_ == 5:
                localctx = RParser.BlockContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 43
                self.match(RParser.T__35)
                self.state = 44
                self.exprlist()
                self.state = 45
                self.match(RParser.T__36)
                pass

            elif la_ == 6:
                localctx = RParser.IfContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 47
                self.match(RParser.T__37)
                self.state = 48
                self.match(RParser.T__33)
                self.state = 49
                self.expr(0)
                self.state = 50
                self.match(RParser.T__34)
                self.state = 51
                self.expr(22)
                pass

            elif la_ == 7:
                localctx = RParser.IfelseContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 53
                self.match(RParser.T__37)
                self.state = 54
                self.match(RParser.T__33)
                self.state = 55
                self.expr(0)
                self.state = 56
                self.match(RParser.T__34)
                self.state = 57
                self.expr(0)
                self.state = 58
                self.match(RParser.T__38)
                self.state = 59
                self.expr(21)
                pass

            elif la_ == 8:
                localctx = RParser.ForContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 61
                self.match(RParser.T__39)
                self.state = 62
                self.match(RParser.T__33)
                self.state = 63
                self.match(RParser.ID)
                self.state = 64
                self.match(RParser.T__40)
                self.state = 65
                self.expr(0)
                self.state = 66
                self.match(RParser.T__34)
                self.state = 67
                self.expr(20)
                pass

            elif la_ == 9:
                localctx = RParser.WhileContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 69
                self.match(RParser.T__41)
                self.state = 70
                self.match(RParser.T__33)
                self.state = 71
                self.expr(0)
                self.state = 72
                self.match(RParser.T__34)
                self.state = 73
                self.expr(19)
                pass

            elif la_ == 10:
                localctx = RParser.RepeatContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 75
                self.match(RParser.T__42)
                self.state = 76
                self.expr(18)
                pass

            elif la_ == 11:
                localctx = RParser.HelpContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 77
                self.match(RParser.T__43)
                self.state = 78
                self.expr(17)
                pass

            elif la_ == 12:
                localctx = RParser.NextContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 79
                self.match(RParser.T__44)
                pass

            elif la_ == 13:
                localctx = RParser.BreakContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 80
                self.match(RParser.T__45)
                pass

            elif la_ == 14:
                localctx = RParser.ParensContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 81
                self.match(RParser.T__33)
                self.state = 82
                self.expr(0)
                self.state = 83
                self.match(RParser.T__34)
                pass

            elif la_ == 15:
                localctx = RParser.IdContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 85
                self.match(RParser.ID)
                pass

            elif la_ == 16:
                localctx = RParser.StringContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 86
                self.match(RParser.STRING)
                pass

            elif la_ == 17:
                localctx = RParser.HexContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 87
                self.match(RParser.HEX)
                pass

            elif la_ == 18:
                localctx = RParser.IntContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 88
                self.match(RParser.INT)
                pass

            elif la_ == 19:
                localctx = RParser.FloatContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 89
                self.match(RParser.FLOAT)
                pass

            elif la_ == 20:
                localctx = RParser.ComplexContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 90
                self.match(RParser.COMPLEX)
                pass

            elif la_ == 21:
                localctx = RParser.NullContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 91
                self.match(RParser.T__46)
                pass

            elif la_ == 22:
                localctx = RParser.NaContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 92
                self.match(RParser.T__47)
                pass

            elif la_ == 23:
                localctx = RParser.InfContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 93
                self.match(RParser.T__48)
                pass

            elif la_ == 24:
                localctx = RParser.NanContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 94
                self.match(RParser.T__49)
                pass

            elif la_ == 25:
                localctx = RParser.TrueContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 95
                self.match(RParser.T__50)
                pass

            elif la_ == 26:
                localctx = RParser.FalseContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 96
                self.match(RParser.T__51)
                pass

            elif la_ == 27:
                localctx = RParser.DotContext(self, localctx)
                self._ctx = localctx
                # _prevctx = localctx
                self.state = 97
                self.match(RParser.T__52)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 154
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 6,
                                                self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    # _prevctx = localctx
                    self.state = 152
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 5,
                                                       self._ctx)
                    if la_ == 1:
                        localctx = RParser.NamespaceContext(self,
                                                            RParser.
                                                            ExprContext(
                                                                self,
                                                                _parentctx,
                                                                _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 100
                        if not self.precpred(self._ctx, 40):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 40)")
                        self.state = 101
                        _la = self._input.LA(1)
                        if not (_la == 5 or _la == 6):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 102
                        self.expr(41)
                        pass

                    elif la_ == 2:
                        localctx = RParser.ExtractContext(self,
                                                          RParser.ExprContext(
                                                              self, _parentctx,
                                                              _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 103
                        if not self.precpred(self._ctx, 39):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 39)")
                        self.state = 104
                        _la = self._input.LA(1)
                        if not (_la == 7 or _la == 8):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 105
                        self.expr(40)
                        pass

                    elif la_ == 3:
                        localctx = RParser.PowerContext(self,
                                                        RParser.ExprContext(
                                                            self, _parentctx,
                                                            _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 106
                        if not self.precpred(self._ctx, 38):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 38)")
                        self.state = 107
                        self.match(RParser.T__8)
                        self.state = 108
                        self.expr(38)
                        pass

                    elif la_ == 4:
                        localctx = (
                            RParser.SeqContext(
                                self,
                                RParser.ExprContext(
                                    self, _parentctx, _parentState))
                        )
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 109
                        if not self.precpred(self._ctx, 36):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 36)")
                        self.state = 110
                        self.match(RParser.T__11)
                        self.state = 111
                        self.expr(37)
                        pass

                    elif la_ == 5:
                        localctx = RParser.UseropContext(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 112
                        if not self.precpred(self._ctx, 35):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 35)")
                        self.state = 113
                        self.match(RParser.USER_OP)
                        self.state = 114
                        self.expr(36)
                        pass

                    elif la_ == 6:
                        localctx = RParser.MuldivContext(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 115
                        if not self.precpred(self._ctx, 34):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 34)")
                        self.state = 116
                        _la = self._input.LA(1)
                        if not (_la == 13 or _la == 14):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 117
                        self.expr(35)
                        pass

                    elif la_ == 7:
                        localctx = RParser.AddsubContext(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 118
                        if not self.precpred(self._ctx, 33):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 33)")
                        self.state = 119
                        _la = self._input.LA(1)
                        if not (_la == 10 or _la == 11):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 120
                        self.expr(34)
                        pass

                    elif la_ == 8:
                        localctx = RParser.CompareContext(self,
                                                          RParser.ExprContext(
                                                              self, _parentctx,
                                                              _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 121
                        if not self.precpred(self._ctx, 32):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(
                                self,
                                "self.precpred(self._ctx, 32)"
                            )
                        self.state = 122
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and (
                                (1 << _la) & 2064384) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 123
                        self.expr(33)
                        pass

                    elif la_ == 9:
                        localctx = RParser.AndContext(self,
                                                      RParser.ExprContext(
                                                          self,
                                                          _parentctx,
                                                          _parentState)
                                                      )
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 124
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(
                                self,
                                "self.precpred(self._ctx, 30)"
                            )
                        self.state = 125
                        _la = self._input.LA(1)
                        if not (_la == 22 or _la == 23):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 126
                        self.expr(31)
                        pass

                    elif la_ == 10:
                        localctx = (
                            RParser.OrContext(self, RParser.ExprContext(
                                self, _parentctx, _parentState)))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 127
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 29)")
                        self.state = 128
                        _la = self._input.LA(1)
                        if not (_la == 24 or _la == 25):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 129
                        self.expr(30)
                        pass

                    elif la_ == 11:
                        localctx = RParser.BtildeContext(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 130
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 27)")
                        self.state = 131
                        self.match(RParser.T__25)
                        self.state = 132
                        self.expr(28)
                        pass

                    elif la_ == 12:
                        localctx = RParser.AssignContext(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 133
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 26)")
                        self.state = 134
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and (
                                (1 << _la) & 8455716864) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 135
                        self.expr(27)
                        pass

                    elif la_ == 13:
                        localctx = RParser.Index2Context(self,
                                                         RParser.ExprContext(
                                                             self, _parentctx,
                                                             _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 136
                        if not self.precpred(self._ctx, 42):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(self,
                                                           "self.precpred"
                                                           "(self._ctx, 42)")
                        self.state = 137
                        self.match(RParser.T__1)
                        self.state = 138
                        self.sublist()
                        self.state = 139
                        self.match(RParser.T__2)
                        self.state = 140
                        self.match(RParser.T__2)
                        pass

                    elif la_ == 14:
                        localctx = RParser.IndexContext(self,
                                                        RParser.ExprContext(
                                                            self, _parentctx,
                                                            _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 142
                        if not self.precpred(self._ctx, 41):
                            from antlr4.error.Errors import (
                                FailedPredicateException)
                            raise FailedPredicateException(
                                self,
                                "self.precpred(self._ctx, 41)"
                            )
                        self.state = 143
                        self.match(RParser.T__3)
                        self.state = 144
                        self.sublist()
                        self.state = 145
                        self.match(RParser.T__2)
                        pass

                    elif la_ == 15:
                        localctx = RParser.CallContext(self,
                                                       RParser.ExprContext(
                                                           self, _parentctx,
                                                           _parentState))
                        self.pushNewRecursionContext(localctx, _startState,
                                                     self.RULE_expr)
                        self.state = 147
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import \
                                FailedPredicateException
                            raise FailedPredicateException(
                                self,
                                "self.precpred(self._ctx, 24)"
                            )
                        self.state = 148
                        self.match(RParser.T__33)
                        self.state = 149
                        self.sublist()
                        self.state = 150
                        self.match(RParser.T__34)
                        pass

                self.state = 156
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 6, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class ExprlistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.ExprContext)
            else:
                return self.getTypedRuleContext(RParser.ExprContext, i)

        def NL(self, i: int = None):
            if i is None:
                return self.getTokens(RParser.NL)
            else:
                return self.getToken(RParser.NL, i)

        def getRuleIndex(self):
            return RParser.RULE_exprlist

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterExprlist"):
                listener.enterExprlist(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitExprlist"):
                listener.exitExprlist(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExprlist"):
                return visitor.visitExprlist(self)
            else:
                return visitor.visitChildren(self)

    def exprlist(self):

        localctx = RParser.ExprlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_exprlist)
        self._la = 0  # Token type
        try:
            self.state = 168
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 11, 21, 26, 33, 34, 36, 38, 40, 42, 43, 44, 45,
                         46, 47, 48, 49, 50, 51, 52, 53, 56, 57, 58, 59, 60,
                         61]:
                self.enterOuterAlt(localctx, 1)
                self.state = 157
                self.expr(0)
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1 or _la == 63:
                    self.state = 158
                    _la = self._input.LA(1)
                    if not (_la == 1 or _la == 63):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 160
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and (
                            (1 << _la) & 4557639893800455168) != 0):
                        self.state = 159
                        self.expr(0)

                    self.state = 166
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [37]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FormlistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def form(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.FormContext)
            else:
                return self.getTypedRuleContext(RParser.FormContext, i)

        def getRuleIndex(self):
            return RParser.RULE_formlist

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFormlist"):
                listener.enterFormlist(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFormlist"):
                listener.exitFormlist(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFormlist"):
                return visitor.visitFormlist(self)
            else:
                return visitor.visitChildren(self)

    def formlist(self):

        localctx = RParser.FormlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_formlist)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.form()
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 54:
                self.state = 171
                self.match(RParser.T__53)
                self.state = 172
                self.form()
                self.state = 177
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def getRuleIndex(self):
            return RParser.RULE_form

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForm"):
                listener.enterForm(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForm"):
                listener.exitForm(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForm"):
                return visitor.visitForm(self)
            else:
                return visitor.visitChildren(self)

    def form(self):

        localctx = RParser.FormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_form)
        try:
            self.state = 184
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 11, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 178
                self.match(RParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 179
                self.match(RParser.ID)
                self.state = 180
                self.match(RParser.T__28)
                self.state = 181
                self.expr(0)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 182
                self.match(RParser.T__54)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.match(RParser.T__52)
                pass
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SublistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sub(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RParser.SubContext)
            else:
                return self.getTypedRuleContext(RParser.SubContext, i)

        def getRuleIndex(self):
            return RParser.RULE_sublist

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSublist"):
                listener.enterSublist(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSublist"):
                listener.exitSublist(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSublist"):
                return visitor.visitSublist(self)
            else:
                return visitor.visitChildren(self)

    def sublist(self):

        localctx = RParser.SublistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_sublist)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.sub()
            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 54:
                self.state = 187
                self.match(RParser.T__53)
                self.state = 188
                self.sub()
                self.state = 193
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SubContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None,
                     invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(RParser.ExprContext, 0)

        def ID(self):
            return self.getToken(RParser.ID, 0)

        def STRING(self):
            return self.getToken(RParser.STRING, 0)

        def getRuleIndex(self):
            return RParser.RULE_sub

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSub"):
                listener.enterSub(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSub"):
                listener.exitSub(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSub"):
                return visitor.visitSub(self)
            else:
                return visitor.visitChildren(self)

    def sub(self):

        localctx = RParser.SubContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_sub)
        try:
            self.state = 213
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 13, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 194
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 195
                self.match(RParser.ID)
                self.state = 196
                self.match(RParser.T__28)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 197
                self.match(RParser.ID)
                self.state = 198
                self.match(RParser.T__28)
                self.state = 199
                self.expr(0)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 200
                self.match(RParser.STRING)
                self.state = 201
                self.match(RParser.T__28)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 202
                self.match(RParser.STRING)
                self.state = 203
                self.match(RParser.T__28)
                self.state = 204
                self.expr(0)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 205
                self.match(RParser.T__46)
                self.state = 206
                self.match(RParser.T__28)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 207
                self.match(RParser.T__46)
                self.state = 208
                self.match(RParser.T__28)
                self.state = 209
                self.expr(0)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 210
                self.match(RParser.T__54)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 211
                self.match(RParser.T__52)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)

                pass
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    def sempred(self, localctx: RuleContext, ruleIndex: int, predIndex: int):
        if self._predicates is None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx: ExprContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 40)

        if predIndex == 1:
            return self.precpred(self._ctx, 39)

        if predIndex == 2:
            return self.precpred(self._ctx, 38)

        if predIndex == 3:
            return self.precpred(self._ctx, 36)

        if predIndex == 4:
            return self.precpred(self._ctx, 35)

        if predIndex == 5:
            return self.precpred(self._ctx, 34)

        if predIndex == 6:
            return self.precpred(self._ctx, 33)

        if predIndex == 7:
            return self.precpred(self._ctx, 32)

        if predIndex == 8:
            return self.precpred(self._ctx, 30)

        if predIndex == 9:
            return self.precpred(self._ctx, 29)

        if predIndex == 10:
            return self.precpred(self._ctx, 27)

        if predIndex == 11:
            return self.precpred(self._ctx, 26)

        if predIndex == 12:
            return self.precpred(self._ctx, 42)

        if predIndex == 13:
            return self.precpred(self._ctx, 41)

        if predIndex == 14:
            return self.precpred(self._ctx, 24)
