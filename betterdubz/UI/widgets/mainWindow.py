from PyQt5.QtWidgets import QMainWindow, QAction
from betterdubz.UI.widgets import editor

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("BetterDubz")
        self.resize(800, 700)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        editorWindow = editor.EditorWindow()
        self.setCentralWidget(editorWindow)
        renderAction = QAction("Render", self)
        renderAction.triggered.connect(editorWindow.renderDubs)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(renderAction)
        self.show()