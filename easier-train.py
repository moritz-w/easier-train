import sys
sys.path.append("./src")

from detector import Detector
from classifier import Classifier


if __name__ == '__main__':
    d = Detector("resource/img/testimage2.png")
    c = Classifier()
    # d.scan(71, 67)
    d.scan (97, 97)
    print (d.summary)
    c.classifyAs(d.colors, "blue")
    print (c.classify([33, 36, 114]))
    print(c.classify([33, 36, 0]))

    d.save("resource/img/out.png")
