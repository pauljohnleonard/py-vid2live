import time
import cv2


cap = cv2.VideoCapture(0)
tstart = time.time() 
cnt = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    key=cv2.waitKey(1)
    if key == 27:
        break
    cnt += 1
    telep = time.time() - tstart
    fps = cnt / telep
    print ( fps )

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()