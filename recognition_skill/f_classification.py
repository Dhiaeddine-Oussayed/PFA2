from keras.models import load_model
from numpy import argmax
import cv2
from pickle import load
from tensorflow import expand_dims

model = load_model('face_recognition_model')

encoder = load(open("encoder.pkl", "rb"))

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

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
        expanded = expand_dims(resized, axis=0)
        prediction = model.predict(expanded)
        inverse_oh = argmax(prediction)
        inverse_oh = inverse_oh.reshape(-1, 1)
        name = encoder.inverse_transform(inverse_oh)
        cv2.putText(frame, str(name), (x + 5, y + 5), font, fontScale, fontColor, thickness, lineType)
    else:
        pass

    cv2.imshow('Face Detector window', frame)
    key = cv2.waitKey(1)
    if key % 256 == 27:  # ESC code
        break


video_capture.release()
cv2.destroyAllWindows()

