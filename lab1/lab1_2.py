import cv2
import numpy as np
import math

def test_board(sy, sx, h, w):
	ssy = int(sy)
	ssx = int(sx)

	if sx < 0:
		ssx = sx+1
	if sx >= w:
		ssx = sx-1
	if sy < 0:
		ssy = sy+1
	if sy >= h:
		ssy = sy-1
	return ssy, ssx

def nearest_neighbor(y, x, r_h, r_w, ratio, img):
	
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
	
	# x, y -> row and column index
	# x + 0.5 => right shift to the correct position we defined
	# * ratio => map coordinate from new image to origin image
	# - 0.5 => left shift to fit coord between two integers (between two column(row) index)
		
	fx = (float)( (x + 0.5) / ratio - 0.5)
	sx = math.floor(fx)
	fx -= sx

	fy = (float)( (y + 0.5) / ratio - 0.5)
	sy = math.floor(fy)
	fy -= sy

	sx = int(sx)
	sy = int(sy)
	min_din = 1e9

	# find nearest neighbor and return 
	if fx <= 0.5 and fy <= 0.5:
		ssy, ssx = test_board(sy, sx, r_h, r_w)
		return img[ssy][ssx]
	elif fx <= 0.5 and fy > 0.5:
		ssy, ssx = test_board(sy+1, sx, r_h, r_w)
		return img[ssy][ssx]
	elif fx > 0.5 and fy <= 0.5:
		ssy, ssx = test_board(sy, sx+1, r_h, r_w)
		return img[ssy][ssx]
	else:
		ssy, ssx = test_board(sy+1, sx+1, r_h, r_w)
		return img[ssy][ssx]

if __name__ == '__main__':
	img = cv2.imread('IU.png', 1)

	height = np.shape(img)[0]
	width = np.shape(img)[1]

	ratio = 3
	r_height = int(height * ratio)
	r_width = int(width * ratio)

	t_img = np.zeros( (r_height, r_width, 3), np.uint8)


	for w in range(r_width):
		for h in range(r_height):
			# ww = w / ratio;
			# hh = h / ratio;
			# t_img[h][w] = img[hh][ww]
			t_img[h][w] = nearest_neighbor(h, w, r_height, r_width, ratio, img)

	cv2.imwrite("lab1_2.jpg", t_img)
	cv2.imshow('My Image', t_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
