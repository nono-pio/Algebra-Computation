from arpeggio import Optional, PTNodeVisitor, ParserPython, RegExMatch as reg, ZeroOrMore, visit_parse_tree

from src import Add, Div, ExprElem, Mul, Neg, Pow


class ExprParseError(Exception):
    pass


# id: [a-zA-Z][a-zA-Z0-9_]*
def id(): return reg("[a-zA-Z][a-zA-Z0-9_]*")


# var: [a-zA-Z](_[a-zA-Z0-9])? x_0y_3
def var(): return reg("[a-zA-Z](_[a-zA-Z0-9])?")


# number: [0-9]+(.[0-9]*)?((eE)(+-)?[0-9]+)?  /// 12e4 12E4 3e-4 3.5e4
def number():
    return reg(r"[0-9]+(\.[0-9]*)?((e|E)(\+|-)?[0-9]+)?")


# expr: expr_add
def expr():
    return [expr_add, "error"]


def _visit_expr(node, children):
    print("expr", node, children, "->", children[0])
    if node.value == "error":
        raise ExprParseError("An error as been found")
    else:
        return children[0]


# expr_add: expr_mul (+- expr_mul)*
def expr_add(): return expr_mul, ZeroOrMore(["+", "-"], expr_mul)


def _visit_expr_add(node, children):
    if len(children) == 1:
        return children[0]

    therms = []
    positif = True
    for child in children:  # children = [expr, +, expr, -, expr, ...]
        if child == '+':
            positif = True
        elif child == '-':
            positif = False
        else:
            therm = child  # +child
            if not positif:
                therm = Neg(therm)  # -child
            therms.append(therm)

    add = Add(*therms)

    print("expr add", node, children, "->", add)
    return add


# expr_mul: expr_pow (*/ expr_pow)*
def expr_mul():
    return expr_pow, ZeroOrMore(["*", "/"], expr_pow)


def _visit_expr_mul(node, children):
    if len(children) == 1:
        return children[0]

    factors = []
    mul = True
    for child in children:  # children = [expr, +, expr, -, expr, ...]
        if child == '*':
            mul = True
        elif child == '/':
            mul = False
        else:
            factor = child  # +child
            if not mul:
                factor = Div(1, factor)  # -child
            factors.append(factor)

    mul = Mul(*factors)

    print("expr mul", node, children, "->", mul)
    return mul


# expr_pow: expr_unary (^ expr_unary)?
def expr_pow():
    return expr_unary, Optional("^", expr_unary)


def _visit_expr_pow(node, children):
    if len(children) == 1:
        return children[0]

    pow = Pow(children[0], children[1])

    print("expr pow", node, children, "->", pow)
    return pow


# expr_unary: (+-)? expr_atom
def expr_unary():
    return Optional(["+", "-"]), expr_atom


def _visit_expr_unary(node, children):
    if len(children) == 1:
        return children[0]

    expr = children[1]
    if children[0] == '-':
        expr = Neg(expr)

    print("expr unary", node, children, "->", expr)
    return expr


# expr_atom: (expr) | number | expr_func (before var) | var
def expr_atom():
    return [("(", expr, ")"), number, expr_func, var]


def _visit_expr_atom(node, children):
    print("expr atom", node, children, "->", children[0])
    return children[0]


# expr_func: id(expr?(,expr)*,?) /// func(expr) func(expr, expr) func(expr,expr,)
def expr_func():
    return id, "(", ZeroOrMore(expr, sep=","), ")"


def _visit_expr_func(node, children):
    print("expr func", node, children)
    return "error"  # TODO


# white-space: ' ' | \n | \t | \r
WS = " \t\n\r"


class ExpressionVisitor(PTNodeVisitor):

    def visit_number(self, node, children):
        print("number", node, children, "->", float(node.value))
        return float(node.value)

    def visit_expr(self, node, children):
        return _visit_expr(node, children)

    def visit_expr_add(self, node, children):
        return _visit_expr_add(node, children)

    def visit_expr_mul(self, node, children):
        return _visit_expr_mul(node, children)

    def visit_expr_pow(self, node, children):
        return _visit_expr_pow(node, children)

    def visit_expr_unary(self, node, children):
        return _visit_expr_unary(node, children)

    def visit_expr_atom(self, node, children):
        return _visit_expr_atom(node, children)

    def visit_expr_func(self, node, children):
        return _visit_expr_func(node, children)


parser = ParserPython(expr, ws=WS, reduce_tree=True)


def parse(string: str) -> ExprElem:
    return visit_parse_tree(parser.parse(string), ExpressionVisitor())


if __name__ == "__main__":
    value = parser.parse("2^4/5")
    print(value.tree_str())

    visitor = ExpressionVisitor()
    result = visit_parse_tree(value, visitor)
    print(result)
