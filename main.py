import cv2
import numpy as np

ESC = 27
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)


detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)



def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)
    print(keypoints)
    return keypoints


def nothing(x):
    pass

cv2.namedWindow('Settings')
cv2.createTrackbar('threshold', 'Settings', 0, 255, nothing)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        gray_face = gray_frame[y:y+h, x:x+w] 
        color_face = frame[y:y+h, x:x+w] 

        # Cut face to eyes
        faceHeight = gray_face.shape[0]

        cut_face = gray_face[int(faceHeight/4):int(faceHeight/1.7), :]
        threshold = cv2.getTrackbarPos('threshold', 'Settings')
        _, cut_face = cv2.threshold(cut_face, threshold, 255, cv2.THRESH_BINARY)

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            face_height = np.size(color_face, 0)  

            if ey < face_height / 2:
                cv2.rectangle(color_face, (ex, ey), (ex+ew, ey+eh), (0, 225, 255), 2)
                eye = color_face[ey:ey+eh, ex:ex+ew]
                keypoints = blob_process(eye, threshold, detector)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    cv2.imshow("Camera", frame)

    if 'cut_face' in globals():
        cv2.imshow("Eyes", cut_face)

    if 'eye' in globals():
        cv2.imshow("Eye", eye)

    k = cv2.waitKey(10)
    if k == ESC & 0xff:
        break

cap.release()
cv2.destroyAllWindows()