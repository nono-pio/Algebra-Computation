from src.core.constructors import Add, Pow, Mul
from src.simplify.expand import expand

if __name__ == '__main__':
    add = Add("x", "x", "y")
    print(add)
    pow = Pow(2, 0.5)
    print(pow)
    print(expand(Mul(Add("x", 3), Add("x", -3)), deep=False))
