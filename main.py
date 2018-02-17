from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

import sys

import PyQt5.Qt as Qt


class AppWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(Qt.QPalette.Base)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.Qt.black)
        self.setPalette(p)

        self.image_label = Qt.QLabel(self)
        self.image_label.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.Qt.AlignCenter)

        self.text_label = Qt.QLabel(self)
        self.text_label.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.text_label.setAlignment(Qt.Qt.AlignCenter)

        self.layout = Qt.QGridLayout()
        self.layout.addWidget(self.image_label, 1, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.text_label, 0, 0)

        self.setLayout(self.layout)
        self.showFullScreen()

    def show_image(self, image_path, is_hotdog):
        if image_path is None:
            return self.image_label.clear()
        pixmap = Qt.QPixmap(image_path)
        height = self._height()
        scaled = pixmap.scaledToHeight(height, Qt.Qt.SmoothTransformation)
        self.image_label.setAlignment(Qt.Qt.AlignCenter)
        if is_hotdog:
            self.text_label.setStyleSheet('QLabel { background-color: green; color: yellow }')
            print("Hotdog")
            self.text_label.setText("Hotdog")
        else:
            self.text_label.setStyleSheet('QLabel { background-color: red; color: yellow }')
            print("Not hotdog!")
            self.text_label.setText("Not hotdog!")
        self.text_label.setFont(Qt.QFont("Sans", 128, Qt.QFont.Bold))
        return self.image_label.setPixmap(scaled)

    def keyPressEvent(self, event):
        #sys.exit()
        self.close()

    def _height(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.height()

    def _width(self):
        screen = Qt.QDesktopWidget().screenGeometry()
        return screen.width()


def predict(filename):
    model = ResNet50(weights='imagenet')
    img = image.load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    decoded = decode_predictions(preds, top=3)[0]
    return decoded[0][1]


def main(filename):
    app =  Qt.QApplication(sys.argv)
    win = AppWindow()

    is_hotdog = predict(filename) == "hotdog"
    win.show_image(filename, is_hotdog)
    sys.exit(app.exec_())


main(sys.argv[1])
