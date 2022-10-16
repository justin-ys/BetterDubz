from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from betterdubz.objects import dubbing
import ffmpeg


class DubViewer(QWidget):
    def __init__(self, dub: dubbing.DubUnit):
        super(DubViewer, self).__init__()
        self.dub = dub
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)
        if dub.audio:
            self.label.setText(dub.audio)
        else:
            self.label.setText("No audio provided")
        button = QPushButton()
        button.setText("click here...")
        button.clicked.connect(self.uploadAudio)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def uploadAudio(self):
        fname = QFileDialog.getOpenFileName(caption="Select an audio file...", filter="Audio (*.wav)")[0]
        if fname:
            self.dub.audio = fname
            self.label.setText(fname.split("/")[-1])