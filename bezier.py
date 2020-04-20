from math import factorial


def ncr(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


def calculate_5pow(args, t=None):
    rt = 1 - t
    return sum((
        ((rt**5) * args[0]),
        (5 * t * (rt**4) * args[1]),
        (10 * (t**2) * (rt**3) * args[2]),
        (10 * (t**3) * (rt**2) * args[3]),
        (5 * (t**4) * rt * args[4]),
        ((t**5) * args[5])
    ))


def bezier_factory(power):
    def calculate(args, t):
        rt = 1 - t
        return sum(ncr(power, i) * (rt**(power - i)) * (t**i) * args[i] for i, value in enumerate(args))
    return calculate


class BezierCalculator:
    def __init__(self, power, steps_count):
        self._power = power
        self._calculate = bezier_factory(power)
        self._steps_count = steps_count
        self._step = 1 / steps_count

    def get_dots(self, curve_basis):
        x_set, y_set = zip(*curve_basis)
        return [
            (self._calculate(x_set, t), self._calculate(y_set, t))
            for t in map(lambda i: i * self._step, range(0, self._steps_count + 1))
        ]

    @property
    def power(self):
        return self._power
