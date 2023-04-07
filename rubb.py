import time
import os
from cv2 import cv2

# print time
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
img_path = r"D:\ANewspace\code\NSRMhand\results\run_2\00003601.jpg"

img_hand = cv2.imread(img_path)

# make image darker
# 使图片变暗
cv2.imshow("hand",img_hand)
cv2.waitKey(0)
