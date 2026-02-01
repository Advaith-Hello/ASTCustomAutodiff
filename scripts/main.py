from parse.parse import parse


# Parses the given expression
AST = parse("5y(4x^2 - 6xy^2 + 9y)")
print(AST)

# Substitutes given values and returns result
result = AST.eval({"x": 3, "y": 4})
print(result)

# Finds the derivative with respect to x
AST_D = AST.diff("x").simplify()
print(AST_D)
