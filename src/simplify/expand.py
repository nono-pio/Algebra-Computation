from src.core.base_class.expr import Expr
from src.core import Add, AddOp, Mul, MulOp, Pow, PowOp


def expand(expr: Expr, deep=True):
    """
    a+b -> a+b
    ()
    """

    if deep:
        expr.set_values([expand(val) for val in expr])

    if isinstance(expr, MulOp):

        additions = []
        rest = []

        for factor in expr.factors:
            if isinstance(factor, AddOp):
                additions.append(factor)
                continue
            rest.append(factor)

        if len(additions) == 0:
            return expr

        addition = additions[0]
        for add in additions[1:]:
            addition = mul_add(addition, add)

        return Add(*[
            Mul(therm, *rest) for therm in addition.therms
        ])

    elif isinstance(expr, PowOp):

        base, exp = expr.base, expr.exp
        if isinstance(base, AddOp) and isinstance(exp, int):
            if len(base.therms) == 2:
                return newton_binomial(base[0], base[1], exp)
            else:
                pass  # multinomial
        return expr
    else:
        return expr


def mul_add(add: Add, add2: Add) -> Add:
    results = []
    for therm in add.therms:
        for therm2 in add2.therms:
            results.append(Mul(therm, therm2))

    return Add(*results)


def newton_binomial(a: Expr, b: Expr, n: int):
    from math import comb

    therms = []
    for k in range(0, n + 1):
        k_per_n = comb(n, k)

        therms.append(Mul(k_per_n, Pow(a, k), Pow(b, n - k)))
    return Add(*therms)
