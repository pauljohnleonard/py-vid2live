import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()


while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame',fgmask)
    cv2.imshow('frame2',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()