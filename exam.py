import numpy as np
import cv2

filename = input("please enter filename: ")
img = cv2.imread(filename,-1)
B,G,R=cv2.split(img)

cv2.imshow("Red", R)
cv2.imshow("Grean", G)
cv2.imshow("Blue", B)

cv2.imshow("Lenna", cv2.merge([B,G,R]))
cv2.waitKey(0)