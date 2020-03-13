import cv2
import numpy as np

img = cv2.imread('IU.png', 1)

height = np.shape(img)[0]
width = np.shape(img)[1]

ratio = 3
r_height = height * ratio
r_width = width * ratio

t_img = np.zeros( (r_height, r_width, 3), np.uint8)


for w in range(r_width):
	for h in range(r_height):
		ww = w / ratio;
		hh = h / ratio;

		t_img[h][w] = img[hh][ww]

cv2.imwrite("lab1_2.jpg", t_img)
cv2.imshow('My Image', t_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
