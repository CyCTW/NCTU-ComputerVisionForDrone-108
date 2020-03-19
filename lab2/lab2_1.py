import cv2
import numpy as np
import math

if __name__ == '__main__':
			
	img = cv2.imread('src/mj.tif', 0)
	# print(np.shape(img))

	hh = np.shape(img)[0]
	ww = np.shape(img)[1]

	inten = [0 for i in range(256)]

	n_pixel = ww * hh
	for w in range(ww):
		for h in range(hh):
			inten[ img[h][w] ] += 1;
			# inten_sum += img[h][w]
	
	for i in range(1, 256):
		inten[i] += inten[i-1]
	for i in range(256):
		inten[i] = int(inten[i] / float(n_pixel) * 255)
	
	for w in range(ww):
		for h in range(hh):
			img[h][w] = inten[ img[h][w] ]

	cv2.imwrite("img/lab2_1.jpg", img)
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

