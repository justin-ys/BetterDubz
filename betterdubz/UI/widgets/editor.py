from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsSceneMouseEvent, \
    QStyleOptionGraphicsItem, QGraphicsItem, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtCore import QUrl, QSizeF, Qt, QPoint, QRect, pyqtSignal, QEvent
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainter, QCursor
from betterdubz.UI.widgets import timeline, dubViewer
from betterdubz.objects import dubbing

class PlayerWidget(QGraphicsVideoItem):
    selected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lastClicked = QPoint(0,0)
        self.selectedBR = QPoint(0,0)
        self._states = {"IDLE": 0, "SELECTING": 1, "SELECTED": 2}
        self._state = self._states["IDLE"]
        self.installEventFilter(self)
        self.setFlags(self.flags() | QGraphicsItem.ItemIsFocusable)
        self.isSelected = False

    def mapScreenToVid(self, pos: QPoint):
        view = self.scene().views()[0]
        sceneCoord = self.mapToScene(self.boundingRect().topLeft().toPoint())
        itemPos = view.viewport().mapToGlobal(view.mapFromScene(sceneCoord.toPoint()))
        boundingWidth = (self.boundingRect().right() - self.boundingRect().left())
        offsetX = self.size().width() - boundingWidth
        boundingHeight = (self.boundingRect().bottom() - self.boundingRect().top())
        offsetY = self.size().height() - boundingHeight
        itemPos.setX(int(itemPos.x() - offsetX / 2))
        itemPos.setY(int(itemPos.y() - offsetY / 2))
        return pos - itemPos

    def mapVidToNative(self, pos: QPoint):
        boundingHeight = (self.boundingRect().bottom() - self.boundingRect().top())
        offsetY = self.size().height() - boundingHeight
        ratioX = self.nativeSize().width() / self.size().width()
        ratioY = self.nativeSize().height()/ self.size().height()
        return QPoint(int(ratioX*pos.x()), int(ratioY*(pos.y() - offsetY / 2)))

    def getSelection(self):
        if not (self._state == self._states["SELECTED"]):
            return QRect(QPoint(-1, -1), QPoint(-1, -1))
        return QRect(
            self.mapVidToNative(self.mapScreenToVid(self.lastClicked)),
            self.mapVidToNative(self.mapScreenToVid(self.selectedBR)))

    def clearSelection(self):
        self._state = self._states["IDLE"]
        self.isSelected = False
        self.update()

    def mousePressEvent(self, ev: QGraphicsSceneMouseEvent):
        if ev.button() == Qt.LeftButton:
            self.lastClicked = ev.screenPos()
            self._state = self._states["SELECTING"]
        self.setFocus()

    def mouseReleaseEvent(self, ev: 'QGraphicsSceneMouseEvent'):
        if (self._state == self._states["SELECTING"]) and (ev.button() == Qt.LeftButton):
            self._state = self._states["SELECTED"]
            self.selectedBR = ev.screenPos()
            self.isSelected = True
            self.selected.emit()

    def mouseMoveEvent(self, ev):
        self.update()

    def keyPressEvent(self, ev):
        super().keyPressEvent(ev)
        if ev.type() == QEvent.KeyPress:
            if self._state == self._states["SELECTED"]:
                if ev.key() == Qt.Key_Escape:
                    self.clearSelection()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget = ...):
        super().paint(painter, option, widget)
        if self._state == self._states["SELECTING"]:
            cpos = QCursor.pos()
            painter.drawRect(QRect(self.mapScreenToVid(self.lastClicked), self.mapScreenToVid(cpos)))
        elif self._state == self._states["SELECTED"]:
            painter.drawRect(QRect(self.mapScreenToVid(self.lastClicked), self.mapScreenToVid(self.selectedBR)))


class DubDirectory(QListWidget):
    dubClicked = pyqtSignal(dubbing.DubUnit)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dubs = {}
        self.itemClicked.connect(self._onDubClick)

    def addDub(self, dub: dubbing.DubUnit):
        QListWidgetItem(dub.original, self)
        self.dubs[dub.original] = dub

    def _onDubClick(self, item: QListWidgetItem):
        self.dubClicked.emit(self.dubs[item.text()])

class EditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selectionStart = 0
        self.media = "/home/justin/Downloads/w2l_test_f1.mp4"

        player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoItem = PlayerWidget()
        videoItem.setSize(QSizeF(640, 480))
        videoItem.selected.connect(self.beginSelection)
        scene = QGraphicsScene()
        graphicsView = QGraphicsView(scene)
        scene.addItem(videoItem)
        player.setVideoOutput(videoItem)
        player.setMedia(QMediaContent(QUrl.fromLocalFile(self.media)))
        cRect = scene.itemsBoundingRect()
        scene.setSceneRect(cRect)
        editorTimeline = timeline.TimelineWidget(player)
        vbox = QVBoxLayout()
        vbox.addWidget(graphicsView)
        vbox.addWidget(editorTimeline)

        self.dubView = DubDirectory()
        self.dubView.dubClicked.connect(self.dubSelected)
        hbox = QHBoxLayout()
        hbox.addWidget(self.dubView)
        hbox.addLayout(vbox)
        self.currentDubViewer = QWidget()
        vbox_outer = QVBoxLayout()
        vbox_outer.addLayout(hbox)
        vbox_outer.addWidget(self.currentDubViewer)
        self.setLayout(vbox_outer)

        self.player = player
        self.videoItem = videoItem

    def dubSelected(self, dub: dubbing.DubUnit):
        self.player.setPosition(dub.startTime)
        self.setDubViewer(dub)

    def setDubViewer(self, dub):
        viewer = dubViewer.DubViewer(dub)
        self.layout().replaceWidget(self.currentDubViewer, viewer)
        self.currentDubViewer = viewer

    def beginSelection(self):
        self.selectionStart = self.player.position()

    def keyPressEvent(self, ev: QKeyEvent):
        if ev.key() == Qt.Key_Space:
            if (self.player.state() == QMediaPlayer.PlayingState):
                self.player.pause()
            else:
                self.player.play()
        elif ev.key() == Qt.Key_Return:
            if (self.videoItem.isSelected):
                if (self.player.position() > self.selectionStart):
                    dub = dubbing.DubUnit.fromFile(
                        self.media, self.videoItem.getSelection(), self.selectionStart, self.player.position())
                    self.setDubViewer(dub)
                    self.dubView.addDub(dub)
                self.videoItem.clearSelection()
        elif ev.key() == Qt.Key_R:
            print("sending...")
            self.dubView.dubs[list(self.dubView.dubs.keys())[0]].render()


