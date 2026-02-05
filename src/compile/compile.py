from m_ast.nodes import *
from numba import njit



def compile_expr(expr):
    arg_names = []
    def to_code(node):
        if isinstance(node, Const):
            return repr(node.num)
        elif isinstance(node, Var):
            if node.name not in arg_names:
                arg_names.append(node.name)
            return node.name
        elif isinstance(node, Neg):
            return f"(-{to_code(node.val)})"
        elif isinstance(node, Add):
            return "(" + " + ".join(to_code(a) for a in node.args) + ")"
        elif isinstance(node, Mul):
            return "(" + " * ".join(to_code(a) for a in node.args) + ")"
        elif isinstance(node, Div):
            return f"({to_code(node.num)} / {to_code(node.den)})"
        elif isinstance(node, Pow):
            return f"({to_code(node.base)} ** {to_code(node.power)})"
        elif isinstance(node, Log):
            return f"(math.log({to_code(node.arg)}) / math.log({to_code(node.base)}))"
        else:
            raise NotImplementedError(f"Unknown node type {type(node)}")

    code = to_code(expr)
    src = f"def f({', '.join(arg_names)}):\n\treturn {code}"
    ns = {}
    exec(src, ns)
    return njit(ns["f"])
