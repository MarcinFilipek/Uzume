import cv2
import os
import dlib
import time

cap = cv2.VideoCapture(0)
print('Turn on camera...')
time.sleep(2)

name = input("Name person: ")
pathPersonDir = 'Persons/'
if not os.path.isdir(pathPersonDir + name):
    os.mkdir(pathPersonDir + name)

detector = dlib.get_frontal_face_detector()

count_photo = 0
number_of_photos = 150

while True:
    _, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame_gray)
    if len(faces) == 1:
        x1 = faces[0].left()
        y1 = faces[0].top()
        x2 = faces[0].right()
        y2 = faces[0].bottom()
        count_photo += 1
        roi = frame_gray[y1-10:y2+10, x1-10:x2+10]
        print(count_photo)
        cv2.imwrite(pathPersonDir + name + '/{}_{}.jpg'.format(name, count_photo), roi)
    if count_photo == number_of_photos:
        break

cap.release()
cv2.destroyAllWindows()