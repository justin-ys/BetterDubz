import sys
from betterdubz.UI.widgets.mainWindow import MainWindow
from PyQt5.Qt import QApplication
from qt_material import apply_stylesheet

# https://stackoverflow.com/questions/43039048/pyqt5-fails-with-cryptic-message, to catch strange errors
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    apply_stylesheet(app, "light_blue.xml")
    window = MainWindow()
    sys.exit(app.exec_())
