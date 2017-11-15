import numpy as np
import cv2
import time
import diff_player

from pythonosc import udp_client

        
client = udp_client.SimpleUDPClient("127.0.0.1",7000)
      

player = diff_player.DiffPlayer()


cap = cv2.VideoCapture(0)
ret, old_frame = cap.read()

w=old_frame.shape[1]
h=old_frame.shape[0]

nx=12
dx=w//nx
ny=10
dy=h//ny
nn=nx*ny


def ii(x,y):
    return (y // ny )*nx + x // nx



tstart = time.time() 

cnt = 0

while(1):
    ret, frame = cap.read()
    diff=cv2.addWeighted(frame,1.0,old_frame,-1.0,0)
    disp=frame.copy()

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
            vel = player.process(nn-ii-1,val)
            if vel > 0:
                cv2.rectangle(disp,(i1,j1),(i2,j2),(255-2*vel,0,2*vel),3)
 
    cv2.imshow('disp',disp)


    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

    old_frame=frame
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    # print ( fps )


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()