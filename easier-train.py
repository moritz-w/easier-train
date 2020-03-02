import sys
sys.path.append("./src")

from detector import Detector
from classifier import SingleColorClassifier, MultiColorClassifier


if __name__ == '__main__':
    detector = Detector("resource/img/testimage2.png")
    classifier = MultiColorClassifier()
    # d.scan(71, 67)
    detector.scan (97, 97)
    print (detector.summary)

    classifier.classifyAs(detector.colors, "blue")

    for color in detector.colors:
        color = color.tolist()
        cname = classifier.classify(color)
        assert (cname == "blue")

    classifier.writeOutput("resource/colorclasses/class1")

    detector.save("resource/img/out.png")
