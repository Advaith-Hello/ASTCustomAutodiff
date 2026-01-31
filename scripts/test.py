from m_ast.nodes import *


AST_1 = (
    Add(
        Mul(
            Const(2),
            Pow(
                Var("x"),
                Const(3)
            ),
        ),
        Mul(
            Const(4),
            Pow(
                Var("x"),
                Const(2)
            ),
        ),
    )
)

print(AST_1)
print(AST_1.diff("x"))
print(AST_1.diff("x").simplify())
