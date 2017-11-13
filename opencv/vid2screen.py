import numpy as np
import cv2
import time

fil = '/Users/paulleonard/Movies/SEREBRO.mp4'
cap = cv2.VideoCapture(fil)
tstart = time.time() 
cnt = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    cv2.waitKey(30)
    print ( fps )
    


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()