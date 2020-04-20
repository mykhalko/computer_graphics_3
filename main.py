import sys

from bezier import BezierCalculator
from view import (
    App,
    GenericCanvas
)
from model import Model


def main():
    with App(sys.argv) as app:
        calc = BezierCalculator(power=2, steps_count=20)
        model = Model("objects.json")
        windows = GenericCanvas(default_pen_width=1, calc=calc)
        # for figure in model.figures:
        #     for outline in figure.outlines:
        #         curve_outline_dots = calc.get_dots(outline)
        #         windows.draw_outline(curve_outline_dots)


if __name__ == "__main__":
    main()

