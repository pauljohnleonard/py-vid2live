import libjevois as jevois
import cv2
import numpy as np
from diff_player import DiffPlayer

class PythonSandbox:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("sandbox", 1000, jevois.LOG_INFO)
        self.old_frame=None
        self.player=DiffPlayer()

    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR by default. If
        # you need a grayscale image instead, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB()
        # and getCvRGBA():
        frame = inframe.getCvBGR()
        
        w=frame.shape[1]
        h=frame.shape[0]

        nx=12
        dx=w//nx
        ny=10
        dy=h//ny
        nn=nx*ny

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()


        if self.old_frame != None:
            diff=cv2.addWeighted(frame,1.0,self.old_frame,-1.0,0)
            outimg=frame.copy()

            for i in range(nx):
                i1=i*dx
                i2=i1+dx
                for  j in range(ny):
                    j1=j*dy
                    j2=j1+dy
                    sumB=0
                    sumR=0
                    sumG=0
                    ii=i+j*nx
                    roi=diff[j1:j2,i1:i2]
                    val=cv2.mean(roi)
                    vel = self.player.process(nn-ii-1,val)
                    if vel > 0:
                        cv2.rectangle(outimg,(i1,j1),(i2,j2),(255-2*vel,0,2*vel),3)


            # Write a title:
            cv2.putText(outimg, "PJL Python Sandbox", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),
                        1, cv2.LINE_AA)
            
            # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
            fps = self.timer.stop()
            height, width, channels = outimg.shape # if outimg is grayscale, change to: height, width = outimg.shape
            cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

            # Convert our BGR output image to video output format and send to host over USB. If your output image is not
            # BGR, you can use sendCvGRAY(), sendCvRGB(), or sendCvRGBA() as appropriate:
            outframe.sendCvBGR(outimg)

        self.old_frame=frame
