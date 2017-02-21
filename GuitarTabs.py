from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtGui import *
from PyQt4.Qt import *
from ReadInput import *
from subprocess import call
from popplerqt4 import Poppler

def createButton(it, text, movex, connectWith):
    button = QtGui.QPushButton(text, it)
    button.clicked.connect(connectWith)
    button.resize(100, 30)
    button.move(movex, 320)
    button.setDisabled(True)
    return button

def createChecker(it, movex, movey, text):
    checker = QCheckBox(text, it)
    checker.move(movex, movey)
    return checker

SVGname = 'tabs.svg'
PDFname = 'tabs.pdf'

def convertSvgToPng(sizeX, sizeY):
    call(["rsvg", "-f", "pdf", SVGname, PDFname])
    call(["rm", SVGname])

class Help(QWidget):
    def __init__(self, parent= None):
        super(Help, self).__init__()

        self.setWindowTitle("Help")
        self.setFixedHeight(200)
        self.setFixedWidth(300)

        self.titleText = QLabel(self)
        self.titleText.setText("This is help \n blabla \n etc")

class MyPopup(QWidget):
    def __init__(self, parent= None):
        super(MyPopup, self).__init__()

        self.setWindowTitle("Tabs")
        self.setFixedHeight(500)
        self.setFixedWidth(1010)

        doc = Poppler.Document.load(PDFname)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)
        page = doc.page(0)
        self.image = page.renderToImage()

        thumb = QtGui.QLabel()
        thumb.setPixmap(QtGui.QPixmap.fromImage(self.image))
 
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(thumb)
         
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        
        buttonSave = QtGui.QPushButton("Save tabs", self)
        buttonSave.clicked.connect(self.saveTabs)
        vLayout.addWidget(buttonSave)

        buttonExit = QtGui.QPushButton("Close", self)
        buttonExit.clicked.connect(self.close)
        vLayout.addWidget(buttonExit)

        self.setLayout(vLayout)

    def saveTabs(self):
        with open(QFileDialog.getSaveFileName(self, 'Choose file', filter =".png (*.png)"), 'w') as file:
            file = str(file).split("u'")[1].split("')")[0]
            self.image.save(QtCore.QString(file))

class CreateWidget(QWidget):
    def __init__(self, parent):        
        QtGui.QWidget.__init__(self, parent)

        self.textBox = QTextEdit(self)
        self.textBox.resize(600, 300)
        self.textBox.move(10, 10)
        self.textBox.textChanged.connect(self.textEdited)

        self.titleText = QLabel(self)
        self.titleText.setText("Title")
        self.titleText.move(15, 325)

        self.titleBox = QLineEdit(self)
        self.titleBox.resize(220, 30)
        self.titleBox.move(50, 320)

        self.checkBars = createChecker(self, 290, 325, "Bar numbers")
        self.showScale = createButton(self, "Show scale", 400, self.clickedShowScale)
        self.showTabs = createButton(self, "Show tabs", 510, self.clickedShowTabs)

    def clickedShowScale(self):
        print self.textBox.toPlainText()

    def clickedShowTabs(self):
        data, num = parseInput(self.textBox.toPlainText())
        Image, sizeY = prepareOutputPicture(num)
        sizeX = 950
        paintTabs(Image, data)
        if self.checkBars.isChecked():
            drawBarNumbers(Image, num)
        writeTitle(Image, self.titleBox.text())
        saveImage(Image)

        convertSvgToPng(sizeX, sizeY)

        self.widget = MyPopup()
        self.widget.show()

    def textEdited(self):
        if self.textBox.toPlainText():
            self.showScale.setDisabled(False)
            self.showTabs.setDisabled(False)
        else:
            self.showScale.setDisabled(True)
            self.showTabs.setDisabled(True)

def createAction(it, title, shortcut, tip, connectWith):
    action = QtGui.QAction(title, it)
    action.setShortcut(shortcut)
    action.setStatusTip(tip)
    action.triggered.connect(connectWith)
    return action

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.MainWidget = CreateWidget(self) 
        self.setCentralWidget(self.MainWidget)

        self.load = createAction(self, "&Load", "Ctrl+L", 'Load tabs from a file.', self.loadTabs)
        self.save = createAction(self, "&Save", "Ctrl+S", 'Save tabs to a file.', self.saveTabs)
        self.exit = createAction(self, "&Exit", "Ctrl+E", 'Exit program.', self.close)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(self.load)
        fileMenu.addAction(self.save)
        fileMenu.addAction(self.exit)

        self.copy = createAction(self, "&Copy", "Ctrl+C", 'Copy selected text to clipboard.', self.copySelection)
        self.paste = createAction(self, "&Paste", "Ctrl+P", 'Paste text from clipboard.', self.pasteText)

        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(self.copy)
        editMenu.addAction(self.paste)

        self.help = createAction(self, "&Hint", "Ctrl+H", 'Show hint how to write tabs.', self.showHelp)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(self.help)

    def loadTabs(self):
        file = open(QFileDialog.getOpenFileName(self, 'Choose tab file', directory = '~/'), "r")
        self.MainWidget.textBox.setPlainText(file.read())

    def saveTabs(self):
        with open(QFileDialog.getSaveFileName(self, 'Choose tab file'), 'w') as file:
            file.write(self.MainWidget.textBox.toPlainText())

    def copySelection(self):
        self.MainWidget.textBox.copy()

    def pasteText(self):
        self.MainWidget.textBox.paste()

    def showHelp(self):
        self.help = Help()
        self.help.show()

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MainWindow()
    main.setFixedSize(620, 400)
    main.setWindowTitle('GuitarTabs')
    main.show()

    sys.exit(app.exec_())
    call(["rm", PDFname])