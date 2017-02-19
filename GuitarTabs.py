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
    checker.move(movex, 320)
    return checker

class CreateWidget(QWidget):
    def __init__(self, parent):        
        QtGui.QWidget.__init__(self, parent)

        self.textBox = QTextEdit(self)
        self.textBox.resize(600, 300)
        self.textBox.move(10, 10)
        self.textBox.textChanged.connect(self.textEdited)

        self.checkTabs = createChecker(self, 10, "Tabs", True, self.checkedTabs)
        # self.checkTabs.setCheckState(QtCore.Qt.Checked) why error?
        self.checkTones = createChecker(self, 70, "Tones", False, self.checkedTones) 
        self.checkBars = createChecker(self, 170, "Enumerate bars", False, self.checkedBars)
        self.showScale = createButton(self, "Show scale", 400, self.clickedShowScale)
        self.showTabs = createButton(self, "Show tabs", 510, self.clickedShowTabs)

    def checkedTabs(self):
        if self.checkTabs.isChecked():
            self.checkTones.setCheckState(False)

    def checkedTones(self):
        if self.checkTones.isChecked():
            self.checkTabs.setCheckState(False)

    def checkedBars(self):
        return

    def clickedShowScale(self):
        print self.textBox.toPlainText()

    def clickedShowTabs(self):
        data, num = parseInput(self.textBox.toPlainText())
        Image = prepareOutputPicture(num)
        paintTabs(Image, data)
        drawBarNumbers(Image, num)
        writeTitle(Image, 'This is a long title which should be centered really?')
        saveImage(Image)

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
        file = open(QFileDialog.getOpenFileName(self, 'Choose tab file', directory = '~/'), "r")
        self.MainWidget.textBox.setPlainText(file.read())

    def saveTabs(self):
        with open(QFileDialog.getSaveFileName(self, 'Choose tab file'), 'w') as file:
            file.write(self.MainWidget.textBox.toPlainText())

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