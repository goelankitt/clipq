import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

MAX = 5

class ClipqWindow(QMainWindow):

    copied_items = []
    current_clip = 0

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("ClipQ")
        self.setWindowIcon(QIcon('copy_icon.png'))

        self.tray_icon = ClipqSystemTray(QtGui.QIcon('copy_icon.png'), self)
        self.tray_icon.show()
        
        self.initUI()
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)


    def initUI(self):
        self.textLabel = QLabel("Clipboard empty", self)
        self.textLabel.setFont(QtGui.QFont('SansSerif', 6))
        self.textLabel.setAlignment(Qt.AlignCenter)
        if len(self.copied_items) > 0:
            self.textLabel.setText('%s %s' %((self.current_clip+1), self.copied_items[0],))
        else:
            self.textLabel.setText("Nothing to copy :D")

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(centralWidget)     
 
        self.textLabel.setAlignment(QtCore.Qt.AlignCenter) 
        gridLayout.addWidget(self.textLabel, 0, 0)
        
        self.setGeometry(350, 230, 250, 100)

    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        self.copied_items.insert(0, text)
        if len(self.copied_items) == MAX+1:
            self.copied_items.pop(MAX)
        self.current_clip = 0
        self.textLabel.setText('%s %s' %((self.current_clip+1), self.copied_items[0],))
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.hide()
        elif e.key() == QtCore.Qt.Key_Left:
            self.change_clip(-1)
        elif e.key() == QtCore.Qt.Key_Right:
            self.change_clip(1)
        elif e.key() == QtCore.Qt.Key_Up:
            for i in self.copied_items:
                print(i)
    
    def change_clip(self, num):
        if len(self.copied_items) == 0:
            return
        if self.current_clip == 0 and num == -1:
            self.current_clip = len(self.copied_items) - 1
        elif self.current_clip == len(self.copied_items) - 1 and num == 1:
            self.current_clip = 0
        else:
            self.current_clip = self.current_clip + num
        self.textLabel.setText('%s %s' %((self.current_clip+1), self.copied_items[self.current_clip],))


class ClipqSystemTray(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(ClipqSystemTray, self).__init__(icon, parent)
        self.parent = parent
        menu = QtWidgets.QMenu(parent)
        showWindowAction = menu.addAction("Show clips")
        showWindowAction.triggered.connect(self.show_parent)
        exitAction = menu.addAction("Quit")
        exitAction.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(menu)
    
    def show_parent(self, something):
        self.parent.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mainWin = ClipqWindow()
    mainWin.show()
    sys.exit( app.exec_() )