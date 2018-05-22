import numpy as np
import cv2
import time
import circbuffer
import video_server





class Client:


    def __init__(self,dtMs):
        buffer = 20
        nhist = (1000 * buffer) // dtMs

        self.cbuff = circbuffer.CircularBuffer(n=nhist, dtype='complex_')

        self.downSamp = 2
        self.alpha = 0.05

        self.prev = []
        self.halt=False
        self.dirty = False


    def first(self,frame):
        self.h = frame.shape[0]
        self.w = frame.shape[1]
        self.scale = max(self.h, self) / self.h / self.w
        self.hsv = np.zeros_like(frame)
        self.hsv[..., 1] = 255


    def process(self,frame):


        for i in range(self.downSamp):
            frame = cv2.pyrDown(frame)


        self.frame2 = frame

        next = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)

        if len(self.prev) == 0:
            self.first(frame)
            self.prev = next
            return



        flow = cv2.calcOpticalFlowFarneback(self.prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        dir=flow.sum(axis=(0,1))
        # print(dir)
        dirC=complex(dir[0],dir[1])

        self.cbuff.append(dirC)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        self.hsv[...,0] = ang*180/np.pi/2
        self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

        self.rgb = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)

        cv2.line(self.frame2, (self.w//2, self.h//2), (int(dir[0]*self.scale + self.w//2), int(dir[1]*self.scale + self.h//2)), (255, 0, 0), 5)
        fpsStr =   " CPU:     "+ str(int(video_server.cpu_load))
        cv2.putText(self.frame2, fpsStr, (3, self.h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        self.prev = next
        self.dirty=True

    def display(self):
        if self.dirty:
            cv2.imshow('RGB', self.rgb)
            cv2.imshow('frame1', self.frame2)
            self.dirty=False



    def quit(self):
        self.cap.release()
        self.halt = True
        cv2.destroyAllWindows()



cap = cv2.VideoCapture(0)


dtMs=100

client = Client(dtMs)

video_server=video_server.VideoServer(cap=cap,milliPerFrame=dtMs,client=client)

video_server.start()

