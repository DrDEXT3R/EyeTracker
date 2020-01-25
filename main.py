import cv2
import numpy as np


def nothing(x):
    pass


def threshold_setting(img):
    img_height = img.shape[0]
    img_to_set_up = img[int(img_height/4):int(img_height/1.7), :]

    value_from_trackbar = cv2.getTrackbarPos('threshold', 'Settings')
    _, img_to_set_up = cv2.threshold(img_to_set_up, value_from_trackbar, 255, cv2.THRESH_BINARY)
    return value_from_trackbar, img_to_set_up


def blob_detection(img, t):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_img, t, 255, cv2.THRESH_BINARY)

    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)

    points = detector.detect(img)
    return points


## Set up blob detector
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.maxArea = 1600
detector = cv2.SimpleBlobDetector_create(params)


ESC = 27
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


cv2.namedWindow('Settings')
cv2.createTrackbar('threshold', 'Settings', 50, 255, nothing)


cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Mark face

        gray_face = gray_frame[y:y+h, x:x+w] 
        color_face = frame[y:y+h, x:x+w] 

        threshold, eyes_to_set_up = threshold_setting(gray_face)
  
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            face_height = np.size(color_face, 0) 

            # Prevent false detection 
            if ey < (face_height / 2): 
                #cv2.rectangle(color_face, (ex, ey), (ex+ew, ey+eh), (0, 225, 255), 2) # Mark eye
                eye = color_face[ey:ey+eh, ex:ex+ew]

                keypoints = blob_detection(eye, threshold)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Camera", frame)

    if 'eyes_to_set_up' in globals():
        cv2.imshow("Settings", eyes_to_set_up)

    k = cv2.waitKey(10)
    if k == ESC & 0xff:
        break

cap.release()
cv2.destroyAllWindows()