import numpy as np
import cv2
import time
from circbuffer import CircularBuffer



dtMs=100
dt=dtMs/1000.0

buffer=20
nhist=(1000*buffer)//dtMs

cbuff = CircularBuffer(n=nhist,dtype='complex_')


cap = cv2.VideoCapture(0)
cnt = 0
downSamp=2
fpsDisp=0
alpha=0.05
cpu=0


def lowCap():
    ret, frame = cap.read()

    for i in range(downSamp):
        frame = cv2.pyrDown(frame)

    return frame


frame1 = lowCap()
prvs  = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)

h=frame1.shape[0]
w=frame1.shape[1]
scale=max(h,w)/h/w


hsv = np.zeros_like(frame1)
hsv[...,1] = 255

print (frame1.shape)

tLast = time.time()
tNext = tLast+dt

while(1):

    tStart = time.time()

    frame2 =lowCap()


    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    dir=flow.sum(axis=(0,1))

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('RGB', rgb)

    cv2.line(frame2, (w//2, h//2), (int(dir[0]*scale + w//2), int(dir[1]*scale + h//2)), (255, 0, 0), 5)
    fpsStr = "FPS: " + str("%.2f" % round(fpsDisp,1)) + "  CPU:     "+ str(int(cpu))
    cv2.putText(frame2, fpsStr, (3, h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame1', frame2)


    prvs = next

    tNow = time.time()
    dtFps  =  tNow-tStart

    fps = 1.0 / dtFps
    fpsDisp = (1.0 - alpha)*fpsDisp + fps*alpha

    cpu= 100 * dtFps/dt
    # print (fps)

    tNext = tNext + dt
    tWaitMs =  int((tNext - tNow)*1000)

    if tWaitMs > 0 :
        k = cv2.waitKey(tWaitMs) & 0xff
        if k == 27:
            break
    else:
        print(" UNDERFLOW " , -tWaitMs, " mS")


cap.release()
cv2.destroyAllWindows()
