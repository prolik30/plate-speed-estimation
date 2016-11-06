import os

import cv2

plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

cap = cv2.VideoCapture('day.mp4')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output4.mp4', fourcc, 20.0, (640, 480))
out = cv2.VideoWriter('dayoutput1.mp4', fourcc, 5.0, (2048, 1536))

cascade_counter = 1

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # picture, scale, min neighbors, max size of the detected object
    plates = plate_cascade.detectMultiScale(gray, 1.2, 1, maxSize=(120, 45))

    for (x,y,w,h) in plates:
        framepath = os.path.join("CheckHaarResults2", str(cascade_counter) + '.bmp')
        #plate = cv2.adaptiveThreshold(gray[y:y+h, x:x+w], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 1)
        #cv2.imwrite(framepath, plate)
        cv2.imwrite(framepath, frame[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, h+y), (0, 255, 0), 1)
        cascade_counter+=1

    out.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()
