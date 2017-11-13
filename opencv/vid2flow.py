import numpy as np
import cv2
import time

fil = '/Users/paulleonard/Movies/SEREBRO.mp4'
fil = '/Users/paulleonard/Movies/Circle.mp4'
cap = cv2.VideoCapture(fil)
tstart = time.time() 
cnt = 0

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

downsamp = 3

while(1):
    ret, frame2 = cap.read()
    if cnt%downsamp == 0 :
 
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    #   flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.4, 1, 12, 2, 8, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.imshow('frame2',rgb)
        cv2.imshow('frame3',frame2)
        k = cv2.waitKey(1) & 0xff
        prvs = next
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    cv2.waitKey(30)
    print ( fps )


cap.release()
cv2.destroyAllWindows()
