# design for app in pyqt6

# imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu, QHBoxLayout, QTabWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QAction, QFontDatabase, QFont, QPalette, QColor, QPixmap, QImage, QCursor
import sys
import cv2
import numpy as np
import keyboard as kb


# global vars
window_bg_color = '#fffdf7'
eye_color = "0, 0, 255"
face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # Frontal face detection
eye_data = cv2.CascadeClassifier('haarcascade_eye.xml')  # Eyes detection

# class creating simple widget with background coloring
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class ColorButton(QPushButton):

    def __init__(self, R, G, B):
        super(ColorButton, self).__init__()
        self.setText("")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        color = f'background-color: rgb({R},{G},{B}); border: none;' # add button color
        self.setStyleSheet(color)
        self.setFixedSize(40, 40) # button size

        self.bgr_code = f'{B}, {G}, {R}'

        self.clicked.connect(self.buttonColorClick)
    
    def buttonColorClick(self):
        global eye_color # change globar var of eye_color used by opencv code
        eye_color = self.bgr_code


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
        self.menu.setFixedHeight(500)


        self.menuGrid = QGridLayout()
        self.menu.setLayout(self.menuGrid)

        # adding burger menu
        self.iconLabel = QLabel()
        self.pixmap = QPixmap('menu-w.png')
        self.pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.iconLabel.setPixmap(self.pixmap)
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.iconLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.menuGrid.addWidget(self.iconLabel, 0, 0, 1, 2)

        # hover animation on menu
        self.iconLabel.enterEvent = lambda e: self.toggleMenu(150, True)
        self.iconLabel.leaveEvent = lambda e: self.toggleMenu(150, False)

        # adding color buttons
        btn1 = ColorButton(0,0,255)
        btn2 = ColorButton(255,0,0)
        btn3 = ColorButton(0,255,0)
        btn4 = ColorButton(0,0,0)
        btn5 = ColorButton(0,255,255)
        btn6 = ColorButton(255,0,255)
        
        self.menuGrid.addWidget(btn1, 2, 0)
        self.menuGrid.addWidget(btn2, 2, 1)
        self.menuGrid.addWidget(btn3, 3, 0)
        self.menuGrid.addWidget(btn4, 3, 1)
        self.menuGrid.addWidget(btn5, 4, 0)
        self.menuGrid.addWidget(btn6, 4, 1)

        ### cam
        self.video_size = QSize(640, 480)
        self.setup_camera()
        self.cam_label = QLabel()
        self.cam_label.setFixedSize(self.video_size)
        self.cam_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)


        ### layout
        grid.setContentsMargins(0,0,0,0)
        grid.addWidget(self.menu, 1, 0)
        grid.addWidget(self.cam_label, 1, 13, 1, 13)

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

    # capturing camera using cv2
    def setup_camera(self):

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)
    
    # all changes to frames and replacing them in cam_label
    def display_video_stream(self):
        
        _, frame = self.capture.read()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # detect faces
        face_cords = face_data.detectMultiScale(grayscale, 1.3, 5)
        overlay = frame.copy()

        # draw rect on color img
        # img, top-left-point, bottom-right-point, color, thickness
        for (x, y, w, h) in face_cords:
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (113, 204, 46), 2) # face detection check

            # choose specific area to detect eyes (solve problem with detectinf e.g. nose)
            roi_gray = grayscale[y:y+(h//3)*2, x:x+w] 
            roi_color = frame[y:y+(h//3)*2, x:x+w]

            # detect eyes
            eyes = eye_data.detectMultiScale(roi_gray, 1.3, 5)

            for (ex, ey, ew, eh) in eyes:
                # screate eye circles filled
                eye_center = (x + ex + ew//2 + 2, y + ey + eh//2)
                radius = int(round((ew + eh)*0.07))
                cv2.circle(
                    overlay, 
                    eye_center, 
                    radius,
                    tuple(map(int, eye_color.split(', '))), # change text into tuple
                    -1,
                    )
        image_new = cv2.addWeighted(overlay, 0.2, frame, 1 - 0.2, 0)
        image_new = cv2.flip(image_new, -1) # flip frame
        image_new = cv2.rotate(image_new, cv2.cv2.ROTATE_90_CLOCKWISE) # rotate

        im_np = np.transpose(image_new,(1,0,2)).copy() # QtImage transforming from numpy array       

        qimage = QImage(im_np, im_np.shape[1], im_np.shape[0],                                                                                                                                                 
                        QImage.Format.Format_BGR888)                                                                                                                                                                 
        self.cam_label.setPixmap(QPixmap(qimage)) # replacing frame into label   
        

app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()