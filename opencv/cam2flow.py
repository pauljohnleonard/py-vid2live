import numpy as np
import cv2
import time
from skimage import img_as_float


cap = cv2.VideoCapture(0)
tstart = time.time()
cnt = 0
downSamp=2

def lowCap():
    ret, frame = cap.read()

    for i in xrange(downSamp):
        frame = cv2.pyrDown(frame)

    return frame


frame1 = lowCap()
prvs  = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

w=frame1.shape[0]
h=frame1.shape[1]

# prvs1 = np.zeros((frame1.shape[0],frame1.shape[1], 1), np.float32)      # cv2.CreateMat(frame1.shape[0],frame1.shape[0], cv2.CV_32FC1)
# next1 = np.zeros((frame1.shape[0],frame1.shape[1], 1), np.float32)      # cv2.CreateMat(frame1.shape[0],frame1.shape[0], cv2.CV_32FC1)

prvs1=img_as_float(prvs)


hsv = np.zeros_like(frame1)
hsv[...,1] = 255

print (frame1.shape)

while(1):
    frame2 =lowCap()

    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    next1 = img_as_float(next)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    dir=flow.sum(axis=(0,1))
    print(flow)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('RGB', rgb)

    cv2.line(frame2, (0, 0), (w-1, h-1), (255, 0, 0), 5)
    cv2.imshow('frame1', frame2)


    prvs = next
    prvs1 = next1
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    # print (fps)
    k = cv2.waitKey(20) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
