
# file: videoasync.py
import threading
import cv2
import Queue
import time

class VideoServer:
    def __init__(self, cap, client,src=0, milliPerFrame=100, width=None, height=None):
        self.started = False
        self.read_lock = threading.Lock()
        self.que=Queue.Queue()
        self.client=client
        self.milliPerFrame = milliPerFrame
        self.dt = self.milliPerFrame / 1000.0
        self.alpha=0.1
        self.cap=cap

    def start(self):

        self.tLast = time.time()
        self.tNext = self.tLast + self.dt

        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True

        # self.thread = threading.Thread(target=self.update, args=())
        # self.thread.start()

        self.client_thread = threading.Thread(target=self.notify, args=())
        self.client_thread.start()
        self.run()
        return self

    def notify(self):
        while self.started:
            if self.client.halt:
                self.stop()
            else:
                frame=self.que.get()
                self.client.process(frame)


    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.started:
            tStart = time.time()
            ret,frame = self.cap.read()

            self.que.put(frame)


            tNow = time.time()
            dtFps  =  tNow- tStart


            self.cpu_load= 100 * dtFps/self.dt

            # print (fps)

            self.tNext = self.tNext + self.dt
            tWait =  (self.tNext - tNow)

            if tWait > 0 :
               k=cv2.waitKey(int(tWait*1000))
               if k == 27:
                   self.stop()
            else:
                print(" UNDERFLOW " , -tWait, "S")

            self.client.display()


    def stop(self):
        self.started = False
        self.client_thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

