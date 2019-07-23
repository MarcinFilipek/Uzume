from os import times_result

import cv2
import dlib
from NucleoExpander import NucleoExpander
import os
import math
import time

cap = cv2.VideoCapture(int(os.environ['CAMERA_ID']))

detector = dlib.get_frontal_face_detector()
nucleo = NucleoExpander(os.environ['SERIAL_PORT'], 10)
treshold = 25
horizontal_angle = 90
vertical_angle = 150

nucleo.vertical_servo_set_angle(vertical_angle)
nucleo.packetSerial.send_frame()

while True:
    _, frame = cap.read()
    height_frame, width_frame, _ = frame.shape
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
        centerFace_x = math.floor(centerFace_x)
        centerFace_y = math.floor(centerFace_y)
        # if z == 0:
        #     cv2.circle(frame, (centerFace_x, centerFace_y), 5, (0, 0, 255), -1)
        # else:
        #     cv2.circle(frame, (centerFace_x, centerFace_y), 5, (255, 0, 0), -1)

        cv2.line(frame, (int(centerFrame_x), 0), (int(centerFrame_x), int(height_frame)), (0, 0, 255), 2)
        cv2.line(frame, (0, int(centerFrame_y)), (int(width_frame), int(centerFrame_y)), (0, 0, 255), 2)

        cv2.line(frame, (centerFace_x, 0), (centerFace_x, height_frame), (255, 0, 0), 5)
        cv2.line(frame, (0, centerFace_y), (width_frame, centerFace_y), (255, 0, 0), 5)

        if centerFace_x > centerFrame_x + treshold:
            # horizontal_angle -= 2
            horizontal_angle -= int((centerFace_x - centerFrame_x) / 20)
            nucleo.horizontal_servo_set_angle(horizontal_angle)
        if centerFace_x < centerFrame_x - treshold:
            # horizontal_angle += 2
            horizontal_angle += int((centerFrame_x - centerFace_x) / 20)
            nucleo.horizontal_servo_set_angle(horizontal_angle)

        if centerFace_y > centerFrame_y + treshold:
            # vertical_angle += 2
            vertical_angle += int((centerFace_y - centerFrame_y) / 20)
            nucleo.vertical_servo_set_angle(vertical_angle)
        if centerFace_y < centerFrame_y - treshold:
            # vertical_angle -= 2
            vertical_angle -= int((centerFrame_y - centerFace_y) / 20)
            nucleo.vertical_servo_set_angle(vertical_angle)

        nucleo.packetSerial.send_frame()
        time.sleep(0.01)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()