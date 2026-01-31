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
    def __init__(self, *args): self.args = args
    def __repr__(self): return f"Add{tuple(self.args)}"
    def __str__(self): return "(" + " + ".join(map(str, self.args)) + ")"

    def eval(self, env): return sum([arg.eval(env) for arg in self.args])
    def diff(self, d_var): return Add(*[arg.diff(d_var) for arg in self.args])

    def simplify(self):
        args = [arg.simplify() for arg in self.args]
        new_args = []
        c_sum = 0

        flat = []
        for arg in args:
            if isinstance(arg, Add):
                flat += arg.args
            else:
                flat.append(arg)

        for arg in flat:
            if isinstance(arg, Const):
                c_sum += arg.num
            else:
                new_args.append(arg)

        if c_sum != 0:
            new_args.append(Const(c_sum))

        if len(new_args) == 0:
            return Const(0)
        elif len(new_args) == 1:
            return new_args[0]

        return Add(*new_args)


class Mul(ExprNode):
    def __init__(self, *args): self.args = args
    def __repr__(self): return f"Mul{tuple(self.args)}"
    def __str__(self): return "(" + " * ".join(map(str, self.args)) + ")"

    def eval(self, env): return math.prod([arg.eval(env) for arg in self.args])
    def diff(self, d_var):
        if len(self.args) == 0:
            return Const(0)
        if len(self.args) == 1:
            return self.args[0].diff(d_var)

        terms = []
        for i in range(len(self.args)):
            term_factors = []
            for j in range(len(self.args)):
                if i == j:
                    term_factors.append(self.args[j].diff(d_var))
                else:
                    term_factors.append(self.args[j])

            terms.append(Mul(*term_factors))

        return terms[0] if len(terms) == 1 else Add(*terms)

    def simplify(self):
        args = [arg.simplify() for arg in self.args]
        new_args = []
        c_prod = 1

        flat = []
        for arg in args:
            if isinstance(arg, Mul):
                flat += arg.args
            else:
                flat.append(arg)

        for arg in flat:
            if isinstance(arg, Const):
                c_prod *= arg.num
                if c_prod == 0:
                    return Const(0)
            else:
                new_args.append(arg)

        if c_prod != 1:
            new_args.append(Const(c_prod))

        if len(new_args) == 0:
            return Const(1)
        elif len(new_args) == 1:
            return new_args[0]

        return Mul(*new_args)


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
