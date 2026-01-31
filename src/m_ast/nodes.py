import math



class ExprNode:
    def eval(self, env): raise NotImplementedError
    def diff(self, var): raise NotImplementedError
    def simplify(self): return self


class Const(ExprNode):
    def __init__(self, num): self.num = num
    def __repr__(self): return f"Const({self.num})"
    def __str__(self): return f"{self.num}"

    def eval(self, env): return self.num
    def diff(self, var): return Const(0)


class Var(ExprNode):
    def __init__(self, var_name): self.name = var_name
    def __repr__(self): return f"Var({self.name})"
    def __str__(self): return f"{self.name}"

    def eval(self, env): return env[self.name]
    def diff(self, d_var): return Const(1 if self.name == d_var else 0)


class Neg(ExprNode):
    def __init__(self, val): self.val = val
    def __repr__(self): return f"Neg({self.val})"
    def __str__(self): return f"(-{self.val})"

    def eval(self, env): return -self.val.eval(env)
    def diff(self, d_var): return Neg(self.val.diff(d_var))

    def simplify(self):
        val = self.val.simplify()
        if isinstance(val, Const) and val.num == 0:
            return Const(-val.num)
        if isinstance(val, Neg):
            return val.val

        return Neg(val)


class Add(ExprNode):
    def __init__(self, a, b): self.a, self.b = a, b
    def __repr__(self): return f"Add({self.a}, {self.b})"
    def __str__(self): return f"({self.a} + {self.b})"

    def eval(self, env): return self.a.eval(env) + self.b.eval(env)
    def diff(self, d_var): return Add(self.a.diff(d_var), self.b.diff(d_var))

    def simplify(self):
        a, b = self.a.simplify(), self.b.simplify()
        if isinstance(a, Const) and a.num == 0:
            return b
        if isinstance(b, Const) and b.num == 0:
            return a
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.num + b.num)

        return Add(a, b)


class Mul(ExprNode):
    def __init__(self, a, b): self.a, self.b = a, b
    def __repr__(self): return f"Mul({self.a}, {self.b})"
    def __str__(self): return f"({self.a} * {self.b})"

    def eval(self, env): return self.a.eval(env) * self.b.eval(env)
    def diff(self, d_var): return Add(
        Mul(self.a.diff(d_var), self.b),
        Mul(self.a, self.b.diff(d_var)),
    )

    def simplify(self):
        a, b = self.a.simplify(), self.b.simplify()
        if isinstance(a, Const) and a.num == 0:
            return Const(0)
        if isinstance(b, Const) and b.num == 0:
            return Const(0)
        if isinstance(a, Const) and a.num == 1:
            return b
        if isinstance(b, Const) and b.num == 1:
            return a
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.num * b.num)

        return Mul(a, b)


class Div(ExprNode):
    def __init__(self, a, b): self.a, self.b = a, b
    def __repr__(self): return f"Div({self.a}, {self.b})"
    def __str__(self): return f"({self.a} / {self.b})"

    def eval(self, env): return self.a.eval(env) / self.b.eval(env)
    def diff(self, d_var): return Div(
        Add(
            Mul(self.a.diff(d_var), self.b),
            Neg(Mul(self.a, self.b.diff(d_var))),
        ),
        Mul(self.b, self.b)
    )

    def simplify(self):
        a, b = self.a.simplify(), self.b.simplify()
        if isinstance(a, Const) and a.num == 0:
            return Const(0)
        if isinstance(b, Const) and b.num == 1:
            return a
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.num / b.num)

        return Div(a, b)


class Pow(ExprNode):
    def __init__(self, base, power): self.base, self.power = base, power
    def __repr__(self): return f"Pow({self.base}, {self.power})"
    def __str__(self): return f"({self.base} ** {self.power})"

    def eval(self, env): return self.base.eval(env) ** self.power.eval(env)
    def diff(self, d_var):
        if isinstance(self.power, Const):
            n = self.power.num
            return Mul(
                Mul(Const(n), Pow(self.base, Const(n - 1))),
                self.base.diff(d_var)
            )
        else:
            raise NotImplementedError

    def simplify(self):
        a, b = self.base.simplify(), self.power.simplify()
        if isinstance(a, Const) and isinstance(b, Const):
            return Const(a.num ** b.num) # Order changed for 0^0
        if isinstance(a, Const) and a.num == 0:
            return Const(0)
        if isinstance(b, Const) and b.num == 0:
            return Const(1)
        if isinstance(a, Const) and a.num == 1:
            return Const(1)
        if isinstance(b, Const) and b.num == 1:
            return a

        return Pow(a, b)
