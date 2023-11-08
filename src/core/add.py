from src.core.base_class.basic import sorted_basics, sorted_list_basics
from src.core.base_class.expr import Expr
import src.core as Core
from src.simplify.simplify import simplify

ADD_IDENTITY = 0


class AddOp(Expr):
    therms: list[Expr]

    def __init__(self, *therms: Expr):
        self.therms = list(therms)

    def __iter__(self):
        return iter(self.therms)

    def __getitem__(self, item):
        return self.therms[item]

    def simple_eval(self, _simplify=True) -> int | Expr:

        seq = self.therms
        if _simplify:
            seq = [simplify(therm) for therm in seq]

        # to form add = coeff + c*expr + ...
        coeff = 0
        therms = {}  # in form x = c*expr

        for therm in seq:

            if isinstance(therm, Core.Number):
                coeff += therm
                continue

            elif isinstance(therm, AddOp):
                seq.extend(therm.therms)
                continue

            elif isinstance(therm, Core.MulOp):
                c, t = therm.as_coeff_mul()

            else:
                c, t = 1, therm

            if t in therms:
                therms[t] += c
            else:
                therms[t] = c

        new_therms = []
        for t, c in therms.items():

            if c == 0:
                continue
            elif c == 1:
                new_therms.append(t)
                continue
            elif isinstance(t, Core.MulOp):
                t.mul_coef(c)
                new_therms.append(t)
            else:
                new_therms.append(Core.Mul(c, t))

        if coeff != 0:
            new_therms.append(coeff)

        # return if less than 2 therms
        if len(new_therms) == 0:
            return 0
        elif len(new_therms) == 1:
            return new_therms[0]

        self.therms = new_therms  # TODO:self.therms = sorted_basics(new_therms)
        return self

    def cmp(self, other):
        return sorted_list_basics(self.therms, other.therms)

    def __repr__(self):
        return ' + '.join([str(therm) for therm in self.therms])
