import time

from parse.parse import parse
from compile.compile import compile_expr



AST = parse("2x^2")
print(repr(AST))

f = compile_expr(AST)
print(f(-10))

s = time.perf_counter()

for i in range(10_000_000):
    f(i)

e = time.perf_counter()
print(e-s)
