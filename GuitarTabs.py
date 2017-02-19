from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ReadInput import *

'''
class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)
'''

def createButton(it, text, movex, connectWith):
    button = QtGui.QPushButton(text, it)
    button.clicked.connect(connectWith)
    button.resize(100, 30)
    button.move(movex, 320)
    button.setDisabled(True)
    return button

def createChecker(it, movex, text, isChecked, connectWith):
    checker = QCheckBox(text, it)
    checker.stateChanged.connect(connectWith)
    checker.setChecked(isChecked)
    checker.move(movex, 320)
    return checker

class CreateWidget(QWidget):
    def __init__(self, parent):        
        super(CreateWidget, self).__init__(parent)

        self.textBox = QTextEdit(self)
        self.textBox.resize(600, 300)
        self.textBox.move(10, 10)
        self.textBox.textChanged.connect(self.textEdited)

        self.checkTabs = createChecker(self, 10, "Tabs", True, self.checkedTabs)
        self.checkTones = createChecker(self, 70, "Tones", False, self.checkedTones) 
        self.checkBars = createChecker(self, 170, "Enumerate bars", False, self.checkedBars)
        self.showScale = createButton(self, "Show scale", 400, self.clickedShowScale)
        self.showTabs = createButton(self, "Show tabs", 510, self.clickedShowTabs)

    def checkedTabs(self):
        return

    def checkedTones(self):
        return

    def checkedBars(self):
        return

    def clickedShowScale(self):
        return

    def clickedShowTabs(self):
        return

    def textEdited(self):
        if self.textBox.toPlainText():
            self.showScale.setDisabled(False)
            self.showTabs.setDisabled(False)
        else:
            self.showScale.setDisabled(True)
            self.showTabs.setDisabled(True)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.MainWidget = CreateWidget(self) 
        self.setCentralWidget(self.MainWidget)

        self.load = QtGui.QAction("&Load", self)
        self.load.setShortcut("Ctrl+L")
        self.load.setStatusTip('Load tabs from a file.')
        self.load.triggered.connect(self.loadTabs)

        self.save = QtGui.QAction("&Save", self)
        self.save.setShortcut("Ctrl+S")
        self.save.setStatusTip('Save tabs to a file.')
        self.save.triggered.connect(self.saveTabs)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(self.load)
        fileMenu.addAction(self.save)

    def loadTabs(self):
        self.MainWidget.textBox.setPlainText("test")

    def saveTabs(self):
        print self.MainWidget.textBox.toPlainText()


        #self.dialogTextBrowser = MyDialog(self)

#    def on_pushButton_clicked(self):
#       self.dialogTextBrowser.exec_()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MainWindow()
    main.setFixedSize(620, 400)
    main.setWindowTitle('GuitarTabs')
    main.show()

    sys.exit(app.exec_())