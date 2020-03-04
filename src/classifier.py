import numpy as np

from formatter import Formatter, JSONFormatter


class SingleColorClassifier:


    def __init__(self):
        self.classes = dict()


    def classifyAs (self, rgbcolors, name: str):

        if isinstance(rgbcolors, np.ndarray):
            rgbcolors = rgbcolors.tolist()

        if name not in self.classes:
            self.classes[name] = {
                'r': [0, 0, 0, 0],
                'g': [0, 0, 0, 0],
                'b': [0, 0, 0, 0]
            }

        channel = self.classes[name]

        for rgbcolor in rgbcolors:
            channel['r'][rgbcolor[0] // 64] |= (1 << (63 - (rgbcolor[0] % 64)))
            channel['g'][rgbcolor[1] // 64] |= (1 << (63 - (rgbcolor[1] % 64)))
            channel['b'][rgbcolor[2] // 64] |= (1 << (63 - (rgbcolor[2] % 64)))


    def classify (self, rgbcolor) -> str:
        _class = None
        for classname, colorclass in self.classes.items():
            inclass = \
                bool(colorclass['r'][rgbcolor[0] // 64] >> (63 - (rgbcolor[0] % 64)) & 1) and \
                bool(colorclass['g'][rgbcolor[1] // 64] >> (63 - (rgbcolor[1] % 64)) & 1) and \
                bool(colorclass['b'][rgbcolor[2] // 64] >> (63 - (rgbcolor[2] % 64)) & 1)

            if inclass:
                _class = classname
                break

        return _class


    def writeOutput (self, filename, formatter: Formatter = JSONFormatter()):
        success = formatter.formatToFile(self.classes, filename)
        if not success:
            print (f"Failed to write output to '{filename}' with formatter '{formatter.name}'")
        return success



class MultiColorClassifier:

    def __init__(self):
        self.classes = {
            "r": [0 for i in range(0, 256)],
            "g": [0 for i in range(0, 256)],
            "b": [0 for i in range(0, 256)],
            "colormasks": {},
            "colormask-reverse-lookup": {}
        }
        self.colormask = 1


    @property
    def classPresent(self):
        return self.colormask > 1


    def classifyAs (self, rgbcolors, name: str):

        if isinstance(rgbcolors, np.ndarray):
            rgbcolors = rgbcolors.tolist()

        if name not in self.classes['colormasks']:
            self.classes['colormasks'][name] = self.colormask
            self.classes['colormask-reverse-lookup'][self.colormask] = name
            self.colormask <<= 1

        colormask = self.classes['colormasks'][name]

        for rgbcolor in rgbcolors:
            self.classes['r'][rgbcolor[0]] |= colormask
            self.classes['g'][rgbcolor[1]] |= colormask
            self.classes['b'][rgbcolor[2]] |= colormask


    def classify (self, rgbcolor):

        colorclass = self.classes['r'][rgbcolor[0]] & \
                     self.classes['g'][rgbcolor[1]] & \
                     self.classes['b'][rgbcolor[2]]

        if colorclass == 0:
            return None

        return self.classes['colormask-reverse-lookup'].get(colorclass)


    def writeOutput (self, filename, formatter: Formatter = JSONFormatter()):
        success = formatter.formatToFile(self.classes, filename)
        if not success:
            print (f"Failed to write output to '{filename}' with formatter '{formatter.name}'")
        return success
