import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QThread, Signal, QObject
from PySide2.QtGui import QTextCursor
from gui_template import Ui_MainWindow
from model import ForestInitializer

class MyStream(QObject):
    textWritten = Signal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    
    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        forest = ForestInitializer()

        sys.stdout = MyStream()
        sys.stdout.textWritten.connect(self.normalOutputWritten)

        

        #self.ui.textBrowser.setText("lol")
        self.ui.pushButton.clicked.connect(lambda: forest.initForest())

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        cursor = self.ui.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui.textBrowser.setTextCursor(cursor)
        self.ui.textBrowser.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())