from math import factorial


def ncr(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


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
