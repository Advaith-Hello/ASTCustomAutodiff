import re

from m_ast.nodes import *
from parse.parse_constants import *
from parse.parse_utils import TokenStream



def parse(expr):
    tokens = build_tokens(expr)
    ts = TokenStream(tokens)
    return parse_expr(ts).simplify()


def build_tokens(expr):
    tokens = []
    prev = ('SKIP', '')
    for token in re.finditer(TOK_REGEX, expr):
        k, v = token.lastgroup, token.group()
        if k == 'SKIP': continue
        if prev[0] in ['NUMBER', 'VAR', 'R_PAREN'] and k in ['NUMBER', 'VAR', 'L_PAREN']:
            tokens.append(('MUL', '*'))

        prev = (k, v)
        tokens.append((k, v))

    return tokens


def parse_expr(ts, min_bp=0):
    tok = ts.next()
    if tok is None:
        raise SyntaxError("Unexpected ending token")

    kind, value = tok

    if kind == 'NUMBER':
        left = Const(float(value))

    elif kind == 'VAR':
        left = Var(value)

    elif kind == 'SUB':
        operand = parse_expr(ts, UNARY_BP)
        left = Neg(operand)

    elif kind == 'L_PAREN':
        left = parse_expr(ts, 0)
        if ts.next()[0] != 'R_PAREN':
            raise SyntaxError("Expected ')'")
    else:
        raise SyntaxError("Unidentified token " + tok)

    while True:
        next_tok = ts.peek()
        if next_tok is None:
            break

        kind, op = next_tok
        if kind not in ('ADD', 'SUB', 'MUL', 'DIV', 'POW'):
            break

        lbp, rbp = BINDING_POWER[op]
        if lbp < min_bp:
            break

        ts.next()
        right = parse_expr(ts, rbp)

        if op == '+':
            left = Add(left, right)
        elif op == '-':
            left = Add(left, Neg(right))
        elif op == '*':
            left = Mul(left, right)
        elif op == '/':
            left = Mul(left, Pow(right, Const(-1)))
        elif op == '^':
            left = Pow(left, right)

    return left
