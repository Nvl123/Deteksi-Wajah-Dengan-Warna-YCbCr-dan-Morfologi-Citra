import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()


    b,g,r = cv2.split(frame)

    blue = cv2.equalizeHist(b)
    green = cv2.equalizeHist(g)
    red = cv2.equalizeHist(r)

    frame2 =cv2.merge((blue,green,red))

    konversi = cv2.cvtColor(frame2, cv2.COLOR_BGR2YCrCb)
    
    
    y, cb, cr = cv2.split(konversi)

    a, bin = cv2.threshold(cb, 150, 255, cv2.THRESH_BINARY)

    size = 5

    matriks_SE =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))

    matriks_SE =matriks_SE.astype(np.uint8)

    erosi = cv2.morphologyEx(bin, cv2.MORPH_ERODE, matriks_SE, iterations=1)
    dilasi = cv2.morphologyEx(erosi, cv2.MORPH_DILATE, matriks_SE, iterations=35)
    closing = cv2.morphologyEx(dilasi, cv2.MORPH_CLOSE, matriks_SE, iterations=60)


    masking = cv2.bitwise_and(bin, closing)

    masking2 = cv2.bitwise_and(frame, frame, mask=masking)

    cv2.imshow("frame", masking2)
    # Menunggu tombol ditekan selama 1 ms
    key = cv2.waitKey(1)
    
    # Break loop jika 'q' ditekan
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
