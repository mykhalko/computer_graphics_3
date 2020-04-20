import json


class Figure:
    def __init__(self, data):
        self.name = data["name"]
        self.multiplier = data["multiplier"]
        self._outlines = data["outlines"]

    @property
    def outlines(self):
        mlt = self.multiplier
        return [
            [(dot["x"] * mlt, dot["y"] * mlt) for dot in line]
            for line in self._outlines
        ]


class Model:
    def __init__(self, path):
        with open(path) as file:
            self._figures = [Figure(data) for data in json.load(file)]

    @property
    def figures(self):
        return self._figures
