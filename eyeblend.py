


# imports
from typing import overload
import cv2
import numpy as np
import keyboard as kb

face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # Frontal face detection
eye_data = cv2.CascadeClassifier('haarcascade_eye.xml')  # Eyes detection

# detecting webcam (for 0 - def cam)
webcam = cv2.VideoCapture(0)
eye_colors = [(0, 0, 0), (255, 185, 116), (117, 118, 255), (147, 67, 232), (148, 184, 0)] # basic colors for eye lens


i = 0 # iteration trough colors array

while True:
    successful_frame_read, frame = webcam.read()

    # grayscale frame
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    face_cords = face_data.detectMultiScale(grayscale, 1.3, 5)
    overlay = frame.copy()

    if kb.is_pressed('c'): # change eye color on 'c' pressed
        if i < 4:
            i += 1
        else:
            i = 0

    # draw rect on color img
    # img, top-left-point, bottom-right-point, color, thickness
    for (x, y, w, h) in face_cords:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (113, 204, 46), 2) 

        # choose specific area to detect eyes (solve problem with detectinf e.g. nose)
        roi_gray = grayscale[y:y+(h//3)*2, x:x+w] 
        roi_color = frame[y:y+(h//3)*2, x:x+w]

        # detect eyes
        eyes = eye_data.detectMultiScale(roi_gray, 1.3, 5)
        
        alpha = 0.2

        for (ex, ey, ew, eh) in eyes:
            # screate eye circles filled
            eye_center = (x + ex + ew//2 + 2, y + ey + eh//2)
            radius = int(round((ew + eh)*0.07))
            cv2.circle(
                overlay, 
                eye_center, 
                radius,
                eye_colors[i], 
                -1,
                )
    image_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)


    # show frames
    cv2.imshow('eye detection', image_new)
    cv2.waitKey(1)
