from numbers import Number

from src.core.base_class.expr import Expr
from src.simplify.simplify import simplify
import src.core as Core


class PowOp(Expr):
    base: Expr
    exp: Expr

    def __init__(self, base: Expr, exp: Expr):
        self.base = base
        self.exp = exp

    def __iter__(self):
        yield self.base
        yield self.exp

    def __getitem__(self, item):
        if item == 0:
            return self.base
        elif item == 1:
            return self.exp
        else:
            raise IndexError(f"{item} is not a valid index in `Pow` (0:base, 1:exp)")

    def __repr__(self):
        return f"{self.base}^{self.exp}"

    def as_coef_exp(self):
        return 1, self  # TODO

    def exp_coef(self, coef: Core.Number):
        self.exp = Core.Mul(self.exp, coef)

    def cmp(self, other):
        cmp_base = self.base.cmp(other.base)
        if cmp_base != 0:
            return self.exp.cmp(other.exp)
        return cmp_base

    def simple_eval(self, _simplify=True):

        base, exp = self.base, self.exp

        if _simplify:
            base = simplify(base)
            exp = simplify(exp)

        base_is_number = isinstance(base, Number)
        exp_is_number = isinstance(exp, Number)

        if base_is_number and exp_is_number:
            return base ** exp

        if base_is_number:
            if base == 0:
                return 0
            elif base == 1:
                return 1

        if exp_is_number:
            if exp == 0:
                return 1
            elif exp == 1:
                return base

        return self
