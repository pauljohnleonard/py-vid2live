
'''
Keys
----
ESC - exit
'''
import numpy as np
import cv2
import colorsys
import math
import trackplayer



lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )


def hsv2bgr(h,s,l):
    rgb=colorsys.hsv_to_rgb(h/256.0, s/256.0,l/256.0)
    return (math.floor(rgb[2]*256),math.floor(rgb[1]*256),math.floor(rgb[0]*256))

max_len = 5
note_on_dist = 30

class Track:
    
    def __init__(self,key,start,player):
        self.key=key
        
        self.pts=[start]
        self.col = hsv2bgr( (key*10)%256 , 255, 256 )
        self.isOn = 0
        self.player=player
       

    def addPoint(self,pt):
        self.pts.append(pt)
        if len(self.pts) > max_len:
            del self.pts[0]
        
        dx = self.pts[-1][0] -self.pts[0][0]
        dy = self.pts[-1][1] -self.pts[0][1] 

        dist = math.sqrt(dx*dx+dy*dy)

        on = dist > note_on_dist

        if not self.isOn and on:
            self.isOn=True
            vel = 127
            self.player.on(self.pts[-1],(dx,dy),vel,self.key)
 
        elif self.isOn and not on:
            self.isOn=False
            self.player.off(self.key)


    def kill(self):
        return
        # print ( "Arghh ",self.key)    



class TrackPlayerApp:

    def __init__(self, video_src ,record ):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = cap = cv2.VideoCapture(video_src) 
        _ret, frame = self.cam.read()
        self.frame_idx = 0
        self.rec=record
        self.keyCnt=0
        # Define the codec and create VideoWriter object
        w=frame.shape[1]
        h=frame.shape[0]
        self.player=trackplayer.TrackPlayer()
        self.player.setWindow( (w,h) )
        if record:
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            self.out = cv2.VideoWriter('output.avi',fourcc, 20.0, (w,h))


    def run(self):
        while True:
            _ret, frame = self.cam.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr.pts[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        tr.kill()
                        continue
                    tr.addPoint((x, y))
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 3, tr.col, -1)
                self.tracks = new_tracks
                for tr in self.tracks:
                    cv2.polylines(vis, [np.int32(tr.pts)] , False, tr.col)

                cv2.putText(vis,  'track count: %d' % len(self.tracks),(20, 20),cv2.FONT_HERSHEY_COMPLEX,1,
                            (255,255,255), 1, 8 )


            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr.pts[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 25, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        start=(x, y)
                        self.keyCnt += 1
                        self.tracks.append(Track(self.keyCnt,start,self.player))


            self.frame_idx += 1
            self.prev_gray = frame_gray
            if self.rec:
                self.out.write(vis)
            cv2.imshow('lk_track', vis)
           
            ch = cv2.waitKey(1)
            if ch == 27:
                self.cam.release()
                self.out.release()
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':

    TrackPlayerApp(video_src=0,record=False).run()
