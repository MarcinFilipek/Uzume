import cv2
import dlib
import numpy as np

from tensorflow.python.keras.models import model_from_json

with open('model_architecture.json', 'r') as f:
    model = model_from_json(f.read())
model.load_weights('model_weights.h5')

detector = dlib.get_frontal_face_detector()

print(model.summary())

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame_gray)

    if len(faces) > 0:
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            roi = frame_gray[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
            roi = cv2.resize(roi, (200, 200))
            cv2.imshow("Video", roi)
            roi = np.reshape(roi, newshape=(-1, 200, 200, 1))
            print(model.predict(roi))
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()