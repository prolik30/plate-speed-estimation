import copy
import os

import numpy as np
import cv2

def checkBoxesIsSimilar(box1, box2):
    if sum(abs(box1 - box2)) > 50:
        return False
    else:
        return True

plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

cap = cv2.VideoCapture('1.mp4')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output3.mp4', fourcc, 20.0, (640, 480))

cascade_counter = 1
tracker = cv2.MultiTracker("KCF")

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    newtracker = cv2.MultiTracker("KCF")

    # picture, scale, min neighbors, max size of the detected object
    plates = plate_cascade.detectMultiScale(gray, 1.3, 0, maxSize=(70, 25))

    ok, boxes = tracker.update(frame)

    for plate in plates:
        ok = tracker.add(frame, tuple(plate))

    # if len(plates) > 0:
    #     for plate in plates:
    #         ok = newtracker.add(frame, tuple(plate))
    #
    #     for plate in plates:
    #         for box in boxes:
    #             if not checkBoxesIsSimilar(box, plate):
    #                 newtracker.add(frame, tuple(box))
    #
    #         # ok = tracker.add(frame, tuple(plates[0]))
    #
    #     ok, newboxes = newtracker.update(frame)
    # else:
    #     newboxes = boxes

    newboxes = boxes

    for newbox in newboxes:
    # for newbox in boxes:
        # framepath = os.path.join("CheckHaarResults2", str(cascade_counter) + '.bmp')
        # cv2.imwrite(framepath, gray[y:y+h, x:x+w])

        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 1)

    out.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #tracker = newtracker

cap.release()
out.release()
cv2.destroyAllWindows()
