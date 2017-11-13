
'''
Keys
----
ESC - exit
'''


from time import clock
import numpy as np
import cv2


lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )


class MyApp:

    def __init__(self, video_src ,rec ):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = cap = cv2.VideoCapture(video_src) 
        _ret, frame = self.cam.read()
        self.frame_idx = 0
        self.rec=rec
        # Define the codec and create VideoWriter object
        if rec:
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            w=frame.shape[0]
            h=frame.shape[1]
            self.out = cv2.VideoWriter('output.avi',fourcc, 20.0, (h,w))



    def run(self):
        while True:
            _ret, frame = self.cam.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 3, ( 255, 0,255), -1)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                cv2.putText(vis,  'track count: %d' % len(self.tracks),(20, 20),cv2.FONT_HERSHEY_COMPLEX,1,
                            (255,255,255), 1, 8 )


            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 25, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


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
    MyApp(0,False).run()
