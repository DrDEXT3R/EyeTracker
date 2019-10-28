import cv2
import numpy as np

ESC = 27
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        gray_face = gray_frame[y:y+h, x:x+w] 
        color_face = frame[y:y+h, x:x+w] 

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            face_height = np.size(color_face, 0)  
            if ey < face_height / 2:
                cv2.rectangle(color_face, (ex, ey), (ex+ew, ey+eh), (0, 225, 255), 2)

    cv2.imshow("Camera", frame)
    k = cv2.waitKey(10)
    if k == ESC & 0xff:
        break

cap.release()
cv2.destroyAllWindows()