import cv2
import numpy as np
import math

if __name__ == '__main__':
	img = cv2.imread('src/HyunBin.jpg', 0)

	hh = np.shape(img)[0]
	ww = np.shape(img)[1]

	maskx = np.array([(-1, 0, 1), (-2, 0, 2), (-1, 0, 1)])
	masky = np.array([(-1, -2, -1), (0, 0, 0), (1, 2, 1)])
	
	t_img_x = np.zeros( (hh-2, ww-2, 1), np.uint8)
	t_img_y = np.zeros( (hh-2, ww-2, 1), np.uint8)

	t_img_total = np.zeros( (hh-2, ww-2, 1), np.uint8)
	inten = [0 for i in range(256)]

	n_pixel = ww * hh
	for w in range(ww):
		for h in range(hh):
			inten[ img[h][w] ] += 1;
	
	for i in range(1, 256):
		inten[i] += inten[i-1]
	for i in range(256):
		inten[i] = int(inten[i] / float(n_pixel) * 255)
	
	#for w in range(ww):
		#for h in range(hh):
			#img[h][w] = inten[ img[h][w] ]

	for w in range(ww-2):	
		for h in range(hh-2):
			
			inten_x = 0
			inten_y = 0
			for i in range(3):
				for j in range(3):
					inten_x += maskx[i][j] * img[h + i][w + j]
					inten_y += masky[i][j] * img[h + i][w + j] 
			if inten_x > 70:
				t_img_x[h][w] = 255
			else:
				t_img_x[h][w] = 0
			
			if inten_y > 70:
				t_img_y[h][w] = 255
			else:
				t_img_y[h][w] = 0
			
	t_img_total = t_img_x + t_img_y
	cv2.imwrite("img/MaskX.jpg", t_img_x)
	cv2.imwrite("img/MaskY.jpg", t_img_y)
	cv2.imwrite("img/Mix.jpg", t_img_total)

	cv2.imshow('MaskX+MaskY', t_img_total)
	cv2.imshow('MaskX', t_img_x)
	cv2.imshow('MaskY', t_img_y)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

					
