TOKEN_SPEC = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('VAR', r'[a-zA-Z]'),
    ('POW', r'\^'),
    ('MUL', r'\*'),
    ('DIV', r'\/'),
    ('ADD', r'\+'),
    ('SUB', r'\-'),
    ('L_PAREN', r'\('),
    ('R_PAREN', r'\)'),
    ('SKIP', r'[ \t]+'),
]

TOK_REGEX = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)

UNARY_BP = 25
BINDING_POWER = {
    '+': (10, 11),
    '-': (10, 11),
    '*': (20, 21),
    '/': (20, 21),
    '^': (30, 29),
}
