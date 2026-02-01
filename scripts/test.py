from parse.parse import parse


AST = parse("7x^9 - 5x^8 + 7x^7 - 6x^6 + 9x^5 - 2x^4 + 3x^3 - 2x^2 + 6x - 8")
print("Original:", AST)

for i in range(10):
    AST = AST.diff("x").simplify()
    print(f"AST (d/dx)^{i+1}:", AST)
