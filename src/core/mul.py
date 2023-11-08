from typing import Tuple

import src.core as Core
from src.core.base_class.basic import sorted_basics, sorted_list_basics
from src.core.base_class.expr import Expr
from src.simplify.simplify import simplify


class MulOp(Expr):
    factors: list[Expr]

    def __init__(self, *factors: Expr):
        self.factors = list(factors)

    def __iter__(self):
        return iter(self.factors)

    def __getitem__(self, item):
        return self.factors[item]

    def as_coeff_mul(self) -> Tuple[Core.Number, Expr]:

        coeff = 1
        rest = []

        for factor in self.factors:

            if isinstance(factor, Core.Number):
                coeff *= factor
            else:
                rest.append(factor)

        return coeff, Core.Mul(*rest)

    def mul_coef(self, coef: Core.Number):

        for factor in self.factors:
            if isinstance(factor, Core.Number):
                factor *= coef
                return

        self.add_factor(coef)

    def add_factor(self, new_factor):

        # TODO:Loop for coef
        self.factors.append(new_factor)
        # TODO:self.factors = sorted_basics(self.factors)

    def cmp(self, other):
        return sorted_list_basics(self.factors, other.factors)

    def __repr__(self):
        return ' * '.join([str(factor) for factor in self.factors])

    def simple_eval(self, _simplify=True) -> Core.Number | Expr:

        seq = self.factors
        if _simplify:
            seq = [simplify(therm) for therm in seq]

        # to form mul = coeff * expr^c * ...
        coeff = 1
        factors = {}  # in form x = expr^c

        for factor in seq:

            if isinstance(factor, Core.Number):
                if factor == 0:
                    return 0
                coeff *= factor
                continue

            elif isinstance(factor, MulOp):
                seq.extend(factor.factors)
                continue

            elif isinstance(factor, Core.PowOp):
                c, f = factor.as_coef_exp()

            else:
                c, f = 1, factor

            if f in factors:
                factors[f] += c
            else:
                factors[f] = c

        new_factors = []
        for f, c in factors.items():

            if c == 0:
                continue
            elif c == 1:
                new_factors.append(f)
                continue
            elif isinstance(f, Core.PowOp):
                f.exp_coef(c)
                new_factors.append(f)
            else:
                new_factors.append(Core.Pow(f, c))

        if coeff != 1:
            new_factors.append(coeff)

        # return if less than 2 factors
        if len(new_factors) == 0:
            return 0
        elif len(new_factors) == 1:
            return new_factors[0]

        self.factors = new_factors  # TODO: self.factors = sorted_basics(new_factors)
        return self
