from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtGui import *
from PyQt4.Qt import *
from ReadInput import *
from subprocess import call
from popplerqt4 import Poppler
import markdown

SVGtabs = 'tabs.svg'
PDFtabs = 'tabs.pdf'
SVGtones = 'tones.svg'
PDFtones = 'tones.pdf'

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

def convertSvgToPng(sizeX, sizeY, svg, pdf):
    call(["rsvg", "-f", "pdf", svg, pdf])
    call(["rm", svg])

class Help(QWidget):
    def __init__(self, parent= None):
        super(Help, self).__init__()

        self.setWindowTitle("Help")
        self.setFixedHeight(475)
        self.setFixedWidth(430)

        self.titleText = QLabel(self)
        self.titleText.move(10, 10)
        file = open('README.md', "r").read()
        html = markdown.markdown(file[:-129], extensions=['markdown.extensions.fenced_code'])
        self.titleText.setText(html)

class PopUp(QWidget):
    def __init__(self, title, Height, Width, picture, useScrollArea):
        super(PopUp, self).__init__()

        self.setWindowTitle(title)
        self.setFixedHeight(Height)
        self.setFixedWidth(Width)

        doc = Poppler.Document.load(picture)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)
        page = doc.page(0)
        self.image = page.renderToImage()

        thumb = QtGui.QLabel()
        thumb.setPixmap(QtGui.QPixmap.fromImage(self.image))

        vLayout = QVBoxLayout(self)

        if useScrollArea:
            scroll = QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setWidget(thumb)
            vLayout.addWidget(scroll)
        else:
            vLayout.addWidget(thumb)

        buttonSave = QtGui.QPushButton("Save tabs", self)
        buttonSave.clicked.connect(self.saveFile)
        vLayout.addWidget(buttonSave)

        buttonExit = QtGui.QPushButton("Close", self)
        buttonExit.clicked.connect(self.close)
        vLayout.addWidget(buttonExit)

        self.setLayout(vLayout)

    def saveFile(self):
        file = QFileDialog.getSaveFileName(self, 'Choose file', filter =".png (*.png)")
        if file:
            self.image.save(QtCore.QString(file))

class CreateWidget(QWidget):
    def __init__(self, parent):        
        QtGui.QWidget.__init__(self, parent)

        self.textBox = QTextEdit(self)
        self.textBox.resize(600, 300)
        self.textBox.move(10, 10)
        self.textBox.cursorPositionChanged.connect(self.textEdited)

        self.cursor = self.textBox.textCursor()

        self.titleText = QLabel(self)
        self.titleText.setText("Title")
        self.titleText.move(15, 325)

        self.titleBox = QLineEdit(self)
        self.titleBox.resize(220, 30)
        self.titleBox.move(50, 320)

        self.checkBars = createChecker(self, 290, 325, "Bar numbers")
        self.showScale = createButton(self, "Show scale", 400, self.clickedShowScale)
        self.showTabs = createButton(self, "Show tabs", 510, self.clickedShowTabs)

        self.format = QtGui.QTextCharFormat()
        self.format.setUnderlineStyle(QtGui.QTextCharFormat.WaveUnderline)
        self.format.setUnderlineColor(QtGui.QColor("red"))

    def checkText(self):
        outputErrors = checkBorders(str(self.textBox.toPlainText()))
        print outputErrors
        
        for error in outputErrors:
            print error
            print self.cursor.hasSelection()
            print self.cursor.anchor()
            print self.cursor.position()
            #
            self.cursor.setPosition(error)
            self.cursor.movePosition(QtGui.QTextCursor.EndOfLine, 1)
            print 'end: ', self.cursor.EndOfLine
            self.cursor.mergeCharFormat(self.format)
            self.cursor.clearSelection()
            print 'fix:'
            print self.cursor.hasSelection()
            print self.cursor.anchor()
            print self.cursor.position()
            print "--------------------"

    def clickedShowScale(self):
        data, num = parseInput(self.textBox.toPlainText())
        tones = getTones(data)
        paintTones(tones)

        convertSvgToPng(1060, 400, SVGtones, PDFtones)

        self.widget = PopUp("Scale", 480, 1060, PDFtones, False)
        self.widget.show()

    def clickedShowTabs(self):
        data, num = parseInput(self.textBox.toPlainText())
        Image, sizeY = prepareOutputPicture(num)
        sizeX = 950
        paintTabs(Image, data)
        if self.checkBars.isChecked():
            drawBarNumbers(Image, num)
        writeTitle(Image, self.titleBox.text())
        saveImage(Image)

        convertSvgToPng(sizeX, sizeY, SVGtabs, PDFtabs)

        self.widget = PopUp("Tabs", 500, 1010, PDFtabs, True)
        self.widget.show()

    def textEdited(self):
        self.checkText()
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

        self.clear = createAction(self, "&Clear", "Ctrl+L", 'Clear all the text.', self.clearText)
        self.copy = createAction(self, "&Copy", "Ctrl+C", 'Copy selected text to clipboard.', self.copySelection)
        self.paste = createAction(self, "&Paste", "Ctrl+P", 'Paste text from clipboard.', self.pasteText)

        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(self.clear)
        editMenu.addAction(self.copy)
        editMenu.addAction(self.paste)

        self.help = createAction(self, "&Hint", "Ctrl+H", 'Show hint how to write tabs.', self.showHelp)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(self.help)

    def loadTabs(self):
        file = QFileDialog.getOpenFileName(self, 'Choose tab file', directory = '~/')
        if file:
            file = open(file, "r")
            self.MainWidget.textBox.setPlainText(file.read())

    def saveTabs(self):
        file = QFileDialog.getSaveFileName(self, 'Choose tab file')
        if file:
            with open(file, 'w') as file:
                file.write(self.MainWidget.textBox.toPlainText())

    def copySelection(self):
        self.MainWidget.textBox.copy()

    def pasteText(self):
        self.MainWidget.textBox.paste()

    def showHelp(self):
        self.help = Help()
        self.help.show()

    def clearText(self):
        self.MainWidget.textBox.clear()

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MainWindow()
    main.setFixedSize(620, 400)
    main.setWindowTitle('GuitarTabs')
    main.show()

    sys.exit(app.exec_())