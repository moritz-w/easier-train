import cv2 as cv
import numpy as np
import colour

import os
import time


class Detector:


    def __init__(self, path=None):
        self._outline = list()
        self._distinctColors = dict()
        self._pixelsvisited = np.zeros((0, 0))
        self.last_scantime = -1.0

        self.orignal_img = None
        self.img = None
        self.imgheight = 0
        self.imgwidth = 0
        self.color_diff_tolerance = 25.0

        if path:
            self.loadimage(path)


    def pixelVisited (self, x, y) -> bool:
        return self._pixelsvisited[y, x] == 1


    def setPixelVisited (self, x, y):
        self._pixelsvisited[y, x] = 1


    def pixelInBound (self, x, y):
        if x < 0 or x >= self.imgwidth:
            return False

        if y < 0 or y >= self.imgheight:
            return False

        return True


    def loadimage (self, path):
        self.img = cv.imread (path)
        self.img = cv.cvtColor(self.img.astype(np.float32) / 255, cv.COLOR_BGR2Lab)
        self.orignal_img = self.img.copy()
        self.imgheight, self.imgwidth, _ = self.img.shape
        self._pixelsvisited = np.zeros ((self.imgheight, self.imgwidth))


    def scan (self, x, y):
        if self.img is None:
            raise ValueError ("No image was loaded!")

        base_color = self.img[y, x]
        pixels = list()
        pixels.append((x, y))

        imgcopy = self.img.copy()

        start = time.time()
        while len(pixels) > 0:
            cur = pixels.pop(-1)

            if not self.pixelInBound (*cur):
                continue

            if self.pixelVisited(*cur):
                continue

            self.setPixelVisited(*cur)

            x, y = cur
            # if delta larger than tolerance add to outline and continue
            color_diff = colour.delta_E(base_color, self.img[y, x], method="CIE 1994")
            if color_diff > self.color_diff_tolerance:
                self._outline.append (cur)
                imgcopy[y, x] = [68, 72, 30]
                imgcopy[y if y + 1 >= self.imgheight else y + 1, x] = [68, 72, 30]
                imgcopy[y if y - 1 < 0 else y - 1, x] = [68, 72, 30]
                imgcopy[y, x if x + 1 >= self.imgwidth else x + 1] = [68, 72, 30]
                imgcopy[y, x if x - 1 < 0 else x - 1] = [68, 72, 30]
                continue

            # expand pixel search and add pixel color
            self._distinctColors[tuple(self.img[y, x])] = color_diff
            pixels.extend (((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)))

        self.last_scantime = time.time() - start
        self.img = imgcopy


    def save (self, path):
        img = (cv.cvtColor(self.img, cv.COLOR_Lab2BGR) * 255).astype(np.uint8)
        cv.imwrite (os.path.abspath(path), img)


    def getCvImage (self, colorspace):
        if colorspace == "lab":
            return self.img
        elif colorspace == "rgb255":
            return (cv.cvtColor(self.img, cv.COLOR_Lab2RGB) * 255).astype(np.uint8)
        elif colorspace == "bgr255":
            return (cv.cvtColor(self.img, cv.COLOR_Lab2BGR) * 255).astype(np.uint8)
        elif colorspace == "rgb":
            return cv.cvtColor(self.img, cv.COLOR_Lab2RGB)
        elif colorspace == "bgr":
            return cv.cvtColor(self.img, cv.COLOR_Lab2BGR)
        else:
            return None


    def reset(self):
        self._distinctColors.clear()
        self._pixelsvisited = np.zeros((self.imgheight, self.imgwidth))
        self.img = self.orignal_img


    @property
    def summary(self):
        return {
            "distinct_colors": len(self._distinctColors),
            "scan_time": self.last_scantime,
            "image": {
                "width": self.imgwidth,
                "height": self.imgheight
            }
        }


    @property
    def outline(self):
        return self._outline


    @property
    def colors (self):
        colorarray = np.array([list(self._distinctColors.keys())])
        return (cv.cvtColor(colorarray, cv.COLOR_Lab2RGB) * 255).astype(int)[0]
