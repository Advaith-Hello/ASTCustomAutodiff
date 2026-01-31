from m_ast.nodes import *


AST_1 = (
    Add(
        Mul(
            Const(3),
            Pow(
                Var("x"),
                Const(4)
            ),
        ),
        Mul(
            Const(2),
            Mul(
                Const(5),
                Pow(
                    Var("y"),
                    Const(3)
                )
            ),
            Pow(
                Var("x"),
                Const(3)
            ),
        ),
        Mul(
            Const(4),
            Var("y"),
            Pow(
                Var("x"),
                Const(2)
            ),
        ),
    )
)

print(AST_1)
print(AST_1.diff("x").simplify())
