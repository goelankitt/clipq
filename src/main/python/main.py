from fbs_runtime.application_context import ApplicationContext, cached_property

import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

MAX = 20

class ClipqWindow(QMainWindow):

    copied_items = []
    current_clip = 0

    def __init__(self, ctx):
        QMainWindow.__init__(self)

        self.ctx = ctx
        self.setWindowTitle("ClipQ")
        self.setWindowIcon(self.ctx.img_icon)

        self.tray_icon = ClipqSystemTray(self.ctx.img_icon, self)
        self.tray_icon.show()
        
        self.initUI()
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)


    def initUI(self):
        self.textLabel = QLabel("Clipboard empty", self)
        self.textLabel.setFont(QFont('SansSerif', 6))
        self.textLabel.setAlignment(Qt.AlignCenter)
        if len(self.copied_items) > 0:
            self.textLabel.setText(self.copied_items[0])
        else:
            self.textLabel.setText("Nothing to copy :D")

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(centralWidget)     
 
        self.textLabel.setAlignment(Qt.AlignCenter) 
        gridLayout.addWidget(self.textLabel, 0, 0)
        
        self.setGeometry(350, 230, 250, 100)

    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        if len(self.copied_items) == 0 or self.copied_items[0] != text:
            self.copied_items.insert(0, text)
            if len(self.copied_items) == MAX+1:
                self.copied_items.pop(MAX)
            self.current_clip = 0
            self.textLabel.setText(self.copied_items[0])
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()
        elif e.key() == Qt.Key_Left:
            self.change_clip(-1)
        elif e.key() == Qt.Key_Right:
            self.change_clip(1)
        elif e.key() == Qt.Key_Return:
            self.copied_items.pop(self.current_clip)
            QApplication.clipboard().setText(self.textLabel.text())
            self.hide()
    
    def change_clip(self, num):
        if len(self.copied_items) == 0:
            return
        if self.current_clip == 0 and num == -1:
            self.current_clip = len(self.copied_items) - 1
        elif self.current_clip == len(self.copied_items) - 1 and num == 1:
            self.current_clip = 0
        else:
            self.current_clip = self.current_clip + num
        self.textLabel.setText(self.copied_items[self.current_clip])


class ClipqSystemTray(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(ClipqSystemTray, self).__init__(icon, parent)
        self.parent = parent
        menu = QMenu(parent)
        showWindowAction = menu.addAction("Show clips")
        showWindowAction.triggered.connect(self.show_parent)
        exitAction = menu.addAction("Quit")
        exitAction.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(menu)
    
    def show_parent(self, something):
        self.parent.show()

class AppContext(ApplicationContext):
    def run(self):
        window = ClipqWindow(self)
        version = self.build_settings['version']
        window.setWindowTitle("clipq v" + version)
        window.show()
        return self.app.exec_()
    
    @cached_property
    def img_icon(self):
        return QIcon(self.get_resource('copyicon.png'))


if __name__ == '__main__':
    appctxt = AppContext()
    appctxt.app.setQuitOnLastWindowClosed(False)
    exit_code = appctxt.run()
    sys.exit(exit_code)