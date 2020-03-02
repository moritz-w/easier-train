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

        r_channel = self.classes[name]['r']
        g_channel = self.classes[name]['g']
        b_channel = self.classes[name]['b']
        for rgbcolor in rgbcolors:
            r_channel[rgbcolor[0] // 64] = r_channel[rgbcolor[0] // 64] | (1 << (rgbcolor[0] % 64))
            g_channel[rgbcolor[1] // 64] = g_channel[rgbcolor[1] // 64] | (1 << (rgbcolor[1] % 64))
            b_channel[rgbcolor[2] // 64] = b_channel[rgbcolor[2] // 64] | (1 << (rgbcolor[2] % 64))


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
