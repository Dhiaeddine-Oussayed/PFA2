from keras.models import load_model
from numpy import argmax
from cv2 import VideoCapture, CascadeClassifier
from cv2.data import haarcascades

model = load_model('face_recognition_model')

face_cascade = CascadeClassifier(haarcascades + 'haarcascade_frontalface_default.xml')
video_capture = VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX
position = (65, 90)
fontScale = 1
fontColor = (0, 255, 0)
thickness = 2
lineType = 2

while 1:
    for_detection = None
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        # for each face on the image detected by OpenCV
        # draw a rectangle around the face
        cv2.rectangle(frame,
                      (x, y),  # start_point
                      (x + w, y + h),  # end_point
                      (255, 0, 0),  # color in BGR
                      2)  # thickness in px
        for_detection = gray[y:y + h, x:w + x]
        if for_detection is not None:
            resized = cv2.resize(for_detection, (200, 200))
            prediction = model.predict(resized)



