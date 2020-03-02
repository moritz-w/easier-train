import numpy as np


class Classifier:


    def __init__(self):
        self.classes = dict()


    def classifyAs (self, rgbcolors, name: str):
        if name not in self.classes:
            self.classes[name] = {
                'r': np.zeros(255),
                'g': np.zeros(255),
                'b': np.zeros(255)
            }

        for rgbcolor in rgbcolors:
            self.classes[name]['r'][rgbcolor[0]] = 1
            self.classes[name]['g'][rgbcolor[1]] = 1
            self.classes[name]['b'][rgbcolor[2]] = 1


    def classify (self, rgbcolor) -> str:
        _class = "unknown"
        for classname, colorclass in self.classes.items():
            inclass = bool(
                int(colorclass['r'][rgbcolor[0]]) &
                int(colorclass['g'][rgbcolor[1]]) &
                int(colorclass['b'][rgbcolor[2]]))

            if inclass:
                _class = classname
                break

        return _class
