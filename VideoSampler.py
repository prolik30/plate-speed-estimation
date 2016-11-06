import getopt
import cv2
import os
import re
import numpy as np
import sys

refPt = []
cropping = False
frame = np.zeros(shape=(1, 1))
inputfile = ''


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, inputfile

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(frame, refPt[len(refPt) - 2], refPt[len(refPt) - 1], (0, 255, 0), 1)
        cv2.imshow(inputfile, frame)


def get_last_index_from_file(filename):
    if os.path.exists(filename):
        goodfile = open(filename, 'r')
        line = ''
        for line in goodfile:
            pass
        last = line
        ind = re.findall(r'\d+.bmp', last)
        c = int(re.split(r'\.', ind[0])[0])
        goodfile.close()
        return c
    else:
        return 1


def main(argv):
    if not argv:
        return

    global inputfile
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file=", "help"])
    except getopt.GetoptError:
        print('VideoTest.py -f <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('VideoTest.py -f <inputfile>\n')
            print('hotkeys:\n')
            print('r - reset the cropping regions\n')
            print('n - go to the next frame\n')
            print('j - jump over 100 frame\n')
            print('g - save all \"good\" plates and go to the next frame\n')
            print('b - save frame as bad and go to the next frame \n')
            print('q - exit\n')

            sys.exit()
        elif opt in ("-f", "--file"):
            inputfile = arg

    print('Input file is ' + inputfile)

    gooddirname = 'Good'
    baddirname = 'Bad'
    global refPt
    global frame

    if not os.path.exists(gooddirname):
        os.mkdir(gooddirname)
    if not os.path.exists(baddirname):
        os.mkdir(baddirname)

    vc = cv2.VideoCapture(inputfile)
    cv2.namedWindow(inputfile)
    cv2.setMouseCallback(inputfile, click_and_crop)

    goodcounter = get_last_index_from_file('Good.dat') + 1
    badcounter = get_last_index_from_file('Bad.dat') + 1

    framecounter = 1
    while vc.isOpened():
        ret, frame = vc.read()
        clone = frame.copy()

        while True:
            # display the image and wait for a keypress
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'frame:' + str(framecounter), (0,25), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow(inputfile, frame)
            key = cv2.waitKey(1) & 0xFF

            # if the 'r' key is pressed, reset the cropping regions
            if key == ord('r'):
                frame = clone.copy()
                refPt.clear()

            # if the 'n' key is pressed, go to the next frame
            elif key == ord('n'):
                refPt.clear()
                framecounter+=1
                break
            # if the 'j' key is pressed, jump over 100 frame
            elif key == ord('j'):
                refPt.clear()
                counter = 100
                while counter > 0:
                    ret, frame = vc.read()
                    counter-=1
                framecounter+=100
                break
            # if the 'g' key is pressed, save all "good" plates and go to the next frame
            elif key == ord('g'):
                goodfile = open('Good.dat', 'a')

                framepath = os.path.join(gooddirname, str(goodcounter) + '.bmp')
                cv2.imwrite(framepath, clone)
                goodfile.write(framepath + ' ' + str(int(len(refPt) / 2)))
                for i in refPt:
                    goodfile.write(' ' + str(i[0]) + ' ' + str(i[1]))
                goodfile.write('\n')
                goodcounter += 1
                refPt.clear()
                framecounter+=1
                goodfile.close()

                break
            # if the 'b' key is pressed, save frame as bad
            elif key == ord('b'):
                badfile = open('Bad.dat', 'a')

                for i in range(0, len(refPt), 2):
                    badfragment = clone[refPt[i][1]:refPt[i+1][1], refPt[i][0]:refPt[i+1][0]].copy()
                    framepath = os.path.join(baddirname, str(badcounter) + '.bmp')
                    cv2.imwrite(framepath, badfragment)
                    badfile.write(framepath + '\n')
                    badcounter += 1

                refPt.clear()
                framecounter+=1
                badfile.close()
                break
            # if the 'q' key is pressed, close all resources and exit
            elif key == ord('q'):
                vc.release()
                cv2.destroyAllWindows()
                return


if __name__ == '__main__':
    main(sys.argv[1:])
