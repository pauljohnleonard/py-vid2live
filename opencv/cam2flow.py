import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
tstart = time.time()
cnt = 0
downSamp=4

def lowCap():
    ret, frame = cap.read()

    for i in xrange(downSamp):
        frame = cv2.pyrDown(frame)

    return frame




frame1 = lowCap()
prvs  = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)


hsv = np.zeros_like(frame1)
hsv[...,1] = 255

print (frame1.shape)

while(1):
    frame2 =lowCap()

    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('RGB', rgb)

    cv2.imshow('frame1', frame2)

    prvs = next
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    cv2.waitKey(10)
    # print (fps)

cap.release()
cv2.destroyAllWindows()
