import cv2
from skimage import img_as_float

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

image1  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

image2 = img_as_float(image1)

cv2.imshow('IMAGE1',image1)
cv2.imshow('IMAGE2', image2)

while(1):
    k = cv2.waitKey(100) & 0xff
    if k == 27:
         break

cap.release()
cv2.destroyAllWindows()
