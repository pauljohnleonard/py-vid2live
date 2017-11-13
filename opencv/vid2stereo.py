import numpy as np
import cv2
import time

fil = '/Users/paulleonard/Movies/SEREBRO.mp4'
cap = cv2.VideoCapture(fil)
tstart = time.time() 
cnt = 0
ready = False
stereo = cv2.StereoBM(ndisparities=16, SADWindowSize=15)
# StereoBM(numDisparities=16, blockSize=15)
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    imgL= frame

    if ready :


        disparity = stereo.compute(imgL,imgR)

        # Display the resulting frame
        cv2.imshow('frame',disparity)
        

    ready = True
    imgR=imgL
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    cv2.waitKey(30)
    print ( fps )
    


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()