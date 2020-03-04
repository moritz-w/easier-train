import sys
import os
sys.path.append("./src")

from detector import Detector
from classifier import SingleColorClassifier, MultiColorClassifier

from PyQt5 import QtWidgets, QtCore, QtGui


def msg_box (title, text):
    msgbox = QtWidgets.QMessageBox()
    msgbox.setWindowTitle(title)
    msgbox.setText(text)
    msgbox.exec()


class Mod:
    classifier = MultiColorClassifier()
    tolerance = 25.0



class EasierTrainMainWnd (QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easier Train")
        self.resize(900, 500)
        self.setCentralWidget(EasierTranWidget())


class EasierTranWidget (QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.imgselection = ImageSelectView()
        self.imgselection.fileList.itemClicked.connect (self.on_image_selected)

        self.classifyview = ClassifyView()

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.imgselection, 20)
        self.hbox.addWidget(self.classifyview, 80)

        self.setLayout(self.hbox)


    def on_image_selected (self, item):
        imgpath = item.data(1)
        self.classifyview.loadImage(imgpath)



class ImageSelectView (QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.vbox = QtWidgets.QVBoxLayout()

        self.fileList = QtWidgets.QListWidget()
        self.scanForImages()

        self.vbox.addWidget(self.fileList)
        self.setLayout(self.vbox)


    def scanForImages (self):
        path = "."
        if len(sys.argv) > 1:
            path = sys.argv[1]

        for file in os.listdir(path):
            if file.endswith(".png"):
                item = QtWidgets.QListWidgetItem(file)
                item.setData(1, os.path.abspath(os.path.join(path, file)))
                self.fileList.addItem (item)


class ClassifyView (QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.saveview = SaveView()
        self.imgview = ImageView()
        self.settingsview = SettingsView()
        self.settingsview.classifySignal.connect (self.classify)
        self.settingsview.setToleranceSignal.connect (self.setTolerance)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.saveview, 10)
        self.vbox.addWidget(self.imgview, 80)
        self.vbox.addWidget(self.settingsview, 10)

        self.setLayout(self.vbox)


    def loadImage (self, path):
        self.imgview.loadImage(path)


    def classify (self, cls):
        self.imgview.classify(cls)


    def setTolerance(self, val):
        self.imgview.setTolerance(val)


class SaveView (QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.saveFileText = QtWidgets.QLineEdit(os.path.join(str(os.path.abspath(os.path.curdir)), "outputfile"))
        self.saveBtn = QtWidgets.QPushButton("Save")
        self.saveBtn.pressed.connect(self.save)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.saveFileText)
        self.hbox.addWidget(self.saveBtn)

        self.setLayout(self.hbox)


    def save (self):
        if not Mod.classifier.classPresent:
            msg_box("Error", "Nothing classified yet!")
            return

        path = self.saveFileText.text()
        success = Mod.classifier.writeToFile(path)
        if not success:
            msg_box("Error", f"Failed to write output to {path}")
        else:
            msg_box("Info", f"Classes written to {path}")


class ImageView (QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.detector = None

        self.layout = QtWidgets.QVBoxLayout ()

        self.image = QtWidgets.QLabel(self)
        self.image.mousePressEvent = self.pixelClicked

        self.layout.addWidget(self.image)
        self.setLayout(self.layout)


    def loadImage (self, path):
        self.detector = Detector(path)
        self.detector.color_diff_tolerance = Mod.tolerance
        self.orignal_image = (self.detector.getCvImage("bgr255"), self.detector.imgwidth, self.detector.imgheight)
        self.showImage(self.orignal_image[0], self.detector.imgwidth, self.detector.imgheight)


    def showImage (self, img, width, height):
        qformat = QtGui.QImage.Format_RGB888

        qimg = QtGui.QImage (img.data, width, height, 3 * width, qformat)
        qimg = qimg.rgbSwapped()

        imgpixmap = QtGui.QPixmap.fromImage(qimg)
        self.image.setPixmap(imgpixmap)
        self.image.setFixedSize(self.image.pixmap().size())


    def restoreImage (self):
        self.showImage(*self.orignal_image)


    def pixelClicked (self, event):
        x = event.pos().x()
        y = event.pos().y()

        if not self.detector:
            print ("Error: No image loaded")
            return

        self.detector.scan(x, y)
        print (self.detector.summary)

        self.showImage(self.detector.getCvImage("bgr255"), self.detector.imgwidth, self.detector.imgheight)


    def setTolerance (self, tolerance):
        Mod.tolerance = tolerance
        self.detector.color_diff_tolerance = Mod.tolerance


    def classify (self, cls):
        if not self.detector:
            msg_box ("Error", "Select an image first!")
            return

        if self.detector.summary.get("distinct_colors") < 1:
            msg_box ("Error", "Select a color blob first!")
            return

        Mod.classifier.classifyAs(self.detector.colors, cls)
        self.restoreImage()
        msg_box("Info", f"Classified selected colors as '{cls}'")


class SettingsView (QtWidgets.QWidget):

    classifySignal = QtCore.pyqtSignal(str)
    setToleranceSignal = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.toleranceSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.toleranceSlider.setSingleStep(1)
        self.toleranceSlider.setSliderPosition(25)
        self.toleranceSlider.setMaximum(50)
        self.toleranceSlider.setTracking(False)

        self.classText = QtWidgets.QLineEdit("classname")
        self.classifyBtn = QtWidgets.QPushButton("Classify")

        self.classText.returnPressed.connect (self.classify)
        self.classifyBtn.pressed.connect(self.classify)
        self.toleranceSlider.valueChanged[int].connect (self.setTolerance)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.toleranceSlider)
        self.hbox.addWidget(self.classText)
        self.hbox.addWidget(self.classifyBtn)

        self.setLayout(self.hbox)


    def classify (self):
        self.classifySignal.emit(self.classText.text())


    def setTolerance (self, val: int):
        self.setToleranceSignal.emit(float(val))


def launch_ui ():
    qapp = QtWidgets.QApplication([])
    wnd = EasierTrainMainWnd()
    wnd.show()
    qapp.exec_()



if __name__ == '__main__':
    launch_ui()
