import numpy as np


class Classifier:


    def __init__(self):
        self.classes = dict()


    def classifyAs (self, rgbcolors, name: str):
        if name not in self.classes:
            self.classes[name] = {
                'r': [0, 0, 0, 0],
                'g': [0, 0, 0, 0],
                'b': [0, 0, 0, 0]
            }

        channel = self.classes[name]

        for rgbcolor in rgbcolors:
            channel['r'][rgbcolor[0] // 64] = channel['r'][rgbcolor[0] // 64] | (1 << (64 - rgbcolor[0] % 64))
            channel['g'][rgbcolor[1] // 64] = channel['g'][rgbcolor[1] // 64] | (1 << (64 - rgbcolor[1] % 64))
            channel['b'][rgbcolor[2] // 64] = channel['b'][rgbcolor[2] // 64] | (1 << (64 - rgbcolor[2] % 64))


    def classify (self, rgbcolor) -> str:
        _class = "unknown"
        for classname, colorclass in self.classes.items():
            inclass = \
                bool(colorclass['r'][rgbcolor[0] // 64] >> (64 - rgbcolor[0] % 64) & 1) and \
                bool(colorclass['g'][rgbcolor[1] // 64] >> (64 - rgbcolor[1] % 64) & 1) and \
                bool(colorclass['b'][rgbcolor[2] // 64] >> (64 - rgbcolor[2] % 64) & 1)

            if inclass:
                _class = classname
                break

        return _class
