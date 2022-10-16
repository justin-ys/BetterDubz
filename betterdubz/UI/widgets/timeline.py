from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QSlider, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class TimelineSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTickInterval(1)

    def setPos(self, value):
        self.blockSignals(True)
        self.setValue(value)
        self.blockSignals(False)

class TimelineWidget(QWidget):
    def __init__(self, player: QMediaPlayer):
        super().__init__()
        self.player = player
        self.slider = TimelineSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self._setPlayerPos)
        self.player.positionChanged.connect(self.updatePos)
        vbox = QVBoxLayout()
        vbox.addWidget(self.slider)
        self.setLayout(vbox)

    def getPos(self):
        return int(self.player.duration()*(self.slider.value()/100))

    def updatePos(self):
        pos = self.player.position()
        try:
            self.slider.setPos(int((pos/self.player.duration())*100))
        except ZeroDivisionError:
            pass

    def _setPlayerPos(self):
        self.player.blockSignals(True)
        self.player.pause()
        self.player.setPosition(self.getPos())
        self.player.blockSignals(False)