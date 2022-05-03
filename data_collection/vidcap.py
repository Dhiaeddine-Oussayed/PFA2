import cv2
fc = cv2.CascadeClassifier(r'data_collection/haarcascade_frontalface_alt.xml')
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
img_counter = 1
img = None
while 1:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = fc.detectMultiScale(gray, 1.1, 4)
    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
        img = frame[y:y+h, x:w+x]
    cv2.imshow("test", frame)
    k = cv2.waitKey(1)
    if k == 27:
        # ESC pressed wait a sec
        print("Escape hit, closing...")
        break
    elif k == 32:
        while img_counter < 1000:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = fc.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                img = frame[y:y + h, x:w + x]
            cv2.imshow("Capture loop!", frame)
            img_name = "opencv_frame_{}.png".format(img_counter)
            if type(img) == type(faces):
                cv2.imwrite(img_name, img)
                cv2.imshow("Captured image!", img)
                print("{} written!".format(img_name))
                img_counter += 1
            else:
                print('there is no face to capture')

cam.release()
cv2.destroyAllWindows()
