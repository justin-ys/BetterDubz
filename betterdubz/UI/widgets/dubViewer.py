from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from betterdubz.objects import dubbing


class DubViewer(QWidget):
    def __init__(self, dub: dubbing.DubUnit):
        super(DubViewer, self).__init__()
        self.dub = dub
        button = QPushButton()
        button.setText("click here...")
        button.clicked.connect(self.uploadAudio)
        vbox = QVBoxLayout()
        vbox.addWidget(button)
        self.setLayout(vbox)

    def uploadAudio(self):
        fname = QFileDialog.getOpenFileName(caption="Select an audio file...", filter="Audio (*.wav)")
        if fname:
            self.dub.audio = fname