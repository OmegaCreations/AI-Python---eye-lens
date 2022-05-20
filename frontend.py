# design for app in pyqt6

# imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu, QHBoxLayout, QTabWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QFontDatabase, QFont, QPalette, QColor, QPixmap
import sys

# global vars
window_bg_color = '#fffdf7'
eye_color = '#000000'


# class creating simple widget with background coloring
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


# main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AI Python - eye lens')
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)

        # window sizing
        self.setFixedSize(QSize(1000, 500))
        
        ### background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(window_bg_color))
        self.setPalette(palette)

        ### menu
        self.menu = Color('#00bbf9')

        menuGrid = QGridLayout()
        self.menu.setLayout(menuGrid)

        # adding burger menu
        self.iconLabel = QLabel()
        self.pixmap = QPixmap('menu-w.png')
        self.pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.iconLabel.setPixmap(self.pixmap)
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        menuGrid.addWidget(self.iconLabel)

        # hover animation on menu
        self.iconLabel.enterEvent = lambda e: self.toggleMenu(150, True)
        self.iconLabel.leaveEvent = lambda e: self.toggleMenu(150, False)

        # adding color buttons


        ### cam
        self.cam = Color('#ffffff')
        


        ### layout
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.menu, 1, 0)
        grid.addWidget(self.cam, 1, 1, 1, 13)

    # menu animation
    def toggleMenu(self, maxWidth, hover): 
        # GET WIDTH
        width = self.menu.width()
        maxExtend = maxWidth
        standard = 70

        # SET MAX WIDTH
        if hover:
            widthExtended = maxExtend

        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.menu, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.animation.start()

    




app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()