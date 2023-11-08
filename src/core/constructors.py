import math

import src.core as Core
from src.simplify.simplify import simplify


def Add(*therms: Core.ExprElem, _simplify=True, evaluate=True):
    # simplify if needed
    if _simplify:
        therms = [simplify(therm) for therm in therms]

    # return if less than 2 therms
    if len(therms) == 0:
        return 0
    elif len(therms) == 1:
        return therms[0]

    add = Core.AddOp(*therms)

    # evaluate if needed
    if evaluate:
        return add.simple_eval(_simplify=False)
    return add


def Sub(a: Core.ExprElem, b: Core.ExprElem, _simplify=True, evaluate=True):
    return Add(a,
               Mul(-1, b, _simplify=_simplify, evaluate=evaluate),
               _simplify=_simplify, evaluate=evaluate)


def Neg(a: Core.ExprElem, _simplify=True, evaluate=True):
    return Mul(-1, a, _simplify=_simplify, evaluate=evaluate)


def Mul(*factors: Core.ExprElem, _simplify=True, evaluate=True):
    # simplify if needed
    if _simplify:
        factors = [simplify(factor) for factor in factors]

    # return if less than 2 factors
    if len(factors) == 0:
        return 1
    elif len(factors) == 1:
        return factors[0]

    mul = Core.MulOp(*factors)

    # evaluate if needed
    if evaluate:
        return mul.simple_eval(_simplify=False)
    return mul


def Div(a: Core.ExprElem, b: Core.ExprElem, _simplify=True, evaluate=True):
    return Mul(a,
               Pow(b, -1, _simplify=_simplify, evaluate=evaluate),
               _simplify=_simplify, evaluate=evaluate)


def Pow(base: Core.ExprElem, exponent: Core.ExprElem, _simplify=True, evaluate=True):
    if _simplify:
        base = simplify(base)
        exponent = simplify(exponent)

    power = Core.PowOp(base, exponent)

    if evaluate:
        return power.simple_eval(_simplify=False)
    return power


def Sqrt(base: Core.ExprElem, n: Core.ExprElem, _simplify=True, evaluate=True):
    return Pow(base,
               Div(1, n, _simplify=_simplify, evaluate=evaluate),
               _simplify=_simplify, evaluate=evaluate)


def Exp(exponent: Core.ExprElem, base: Core.ExprElem = math.e, _simplify=True, evaluate=True):
    return Pow(base, exponent, _simplify=_simplify, evaluate=evaluate)
