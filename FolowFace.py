import cv2
import dlib
from NucleoExpander import NucleoExpander
import os
import math

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
nucleo = NucleoExpander(os.environ['SERIAL_PORT'], 10)
treshold = 100
horizontal_angle = 90
while True:
    _, frame = cap.read()
    width_frame, height_frame, _ = frame.shape
    centerFrame_x = width_frame / 2
    centerFrame_y = height_frame / 2

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame_gray)

    for z, face in zip(range(len(faces)), faces):
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        centerFace_x = (x2 - x1) / 2 + x1
        centerFace_y = (y2 - y1) / 2 + y1
        if z == 0:
            cv2.circle(frame, (math.floor(centerFace_x), math.floor(centerFace_y)), 5, (0, 0, 255), -1)
        else:
            cv2.circle(frame, (math.floor(centerFace_x), math.floor(centerFace_y)), 5, (255, 0, 0), -1)

    cv2.imshow("Video", frame)

    if centerFace_x > centerFrame_x + treshold:
        horizontal_angle += 5
        nucleo.horizontal_servo_set_angle(horizontal_angle)
    if centerFace_x < centerFrame_x - treshold:
        horizontal_angle -= 5
        nucleo.horizontal_servo_set_angle(horizontal_angle)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()