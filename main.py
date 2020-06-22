import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QThread, Signal, QObject
from PySide2.QtGui import QTextCursor
from gui_template import Ui_MainWindow
from model import ForestInitializer

#application_path = os.path.dirname(sys.executable)

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

        sys.stdout = MyStream()
        sys.stdout.textWritten.connect(self.normalOutputWritten)

        self.ui.pushButton.clicked.connect(lambda: self.runForest())

    def runForest(self):
        forest = ForestInitializer()

        if self.ui.textEdit.toPlainText() != "": #NTrees
            forest.ntrees = int(self.ui.textEdit.toPlainText())

        if self.ui.textEdit_2.toPlainText() != "": #MaxDepth
            forest.max_depth = int(self.ui.textEdit_2.toPlainText())

        if self.ui.textEdit_3.toPlainText() != "": #Seed
            forest.seed = int(self.ui.textEdit_3.toPlainText())

        print("Running Random Forest")
        print("NTrees = " + str(forest.ntrees))
        print("Max Depth = " + str(forest.max_depth))
        print("Seed = " + str(forest.seed))

        performance = forest.initForest()

        accuracy = "ACCURACY = " + str(performance[0])
        logloss = "LOGLOSS = " + str(performance[1])
        auc = "AUC = " + str(performance[2])

        summary = "Model Performance:" + "\n\n" + accuracy + "\n\n" + logloss + "\n\n" + auc

        cursor_2 = self.ui.textBrowser_2.textCursor()
        cursor_2.movePosition(QTextCursor.End)
        cursor_2.insertText(summary)

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