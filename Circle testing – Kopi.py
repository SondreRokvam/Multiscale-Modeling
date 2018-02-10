import cv2
import numpy as np


for i in range(1,10):
    img = cv2.imread(r'‪C:\Users\Rockv\Desktop\41fUEiKvDeL.jpg', 0)

    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cimg = cv2.dilate(cimg, (3, 3))  # Fill in gaps from blurring. This helps to detect circles with broken edges.


    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 10, 20,param1 = 100, param2 = 30, minRadius =50, maxRadius = 200)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow('detected circles', cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("one")