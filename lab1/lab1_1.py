import cv2
import numpy as np

img = cv2.imread('kobe.jpg', 1)
# print(np.shape(img))


height = np.shape(img)[0]
width = np.shape(img)[1]
t_img = np.zeros( ( height, width, 1), np.uint8)

for w in range(width):
	for h in range(height):
		gray = 0
		for ch in range(3):
			gray += img[h][w][ch]
		gray /= 3.0
		t_img[h][w][0] = gray		
	
cv2.imwrite("lab1_1.jpg", t_img)

cv2.imshow('My Image', t_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
