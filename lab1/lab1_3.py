import cv2
import numpy as np
import math

# if out of board , use the neighbor's value
def test_board(sy, sx, h, w):
	ssy = sy
	ssx = sx

	if sx < 0:
		ssx = sx+1
	if sx >= w:
		ssx = sx-1
	if sy < 0:
		ssy = sy+1
	if sy >= h:
		ssy = sy-1
	return ssy, ssx
	
def bilinear(y, x, ch, r_h, r_w, ratio, img):

	# # # # # # # # # # # # # 
	# Coordinate Definition #
	#                       #
	#    0  0.5  1  1.5  2  #
	#  0 -----------------  #
	#    |       |       |  #
	#0.5 |       |       |  #
	#    |       |       |  #
	#  1 -----------------  #
	#                       #
	#                       #
	# # # # # # # # # # # # #
	
	fx = (float)( (x + 0.5) / ratio - 0.5)
	# (x+0.5)*ratio => map from coordinate from new image to origin image
	# -0.5 => left shift to fit coord between two integers 
	# (for easily computed)
	
	sx = math.floor(fx)
	fx -= sx

	fy = (float)( (y + 0.5) / ratio - 0.5)
	sy = math.floor(fy)
	fy -= sy

	# sy, sx is the up-left point coordinate	
	ssy, ssx = test_board(sy, sx, r_h, r_w)
	lu = img[int(ssy)][int(ssx)][ch]  
	ssy, ssx = test_board(sy+1, sx, r_h, r_w)
	ld = img[int(ssy) ][int(ssx) ][ch]
	ssy, ssx = test_board(sy, sx+1, r_h, r_w)
	ru = img[int(ssy)][int(ssx) ][ch]
	ssy, ssx = test_board(sy+1, sx+1, r_h, r_w)
	rd = img[int(ssy) ][int(ssx) ][ch]
	
	# first interpolation
	ff1 = (1.0-fx) * lu + (fx) * ru
	ff2 = (1.0-fx) * ld + (fx) * rd
	
	# second interpolation
	ss = fy * ff2 + (1.0-fy) * ff1

	return ss
	
if __name__ == '__main__':
	img = cv2.imread('IU.png', 1)

	height = np.shape(img)[0]
	width = np.shape(img)[1]

	ratio = 0.7;
	r_height, r_width = int(ratio*height), int(ratio*width)

	t_img = np.zeros( (r_height, r_width, 3), np.uint8)


	for h in range(r_height):
		for w in range(r_width):
			for ch in range(3):
				t_img[h][w][ch] = bilinear(h, w, ch, r_height, r_width, ratio, img)
	cv2.imwrite("lab1_3.jpg", t_img)
	cv2.imshow('MyImage', t_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
