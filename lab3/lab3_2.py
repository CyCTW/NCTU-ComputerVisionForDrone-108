import cv2
import numpy as np
import math
import random

set1 = [i for i in range (999999)]

def find_parent(idx):
	if set1[idx] == idx:
		return idx
	else:
		r = find_parent(set1[idx])
		set1[idx] = r
		return r

def union(idx1, idx2):
	root1 = find_parent(idx1)
	root2 = find_parent(idx2)
	
	if root1 > root2:
		set1[root1] = root2
	else:
		set1[root2] = root1

def print_img(img, hh, ww):
	for w in range(ww):
		for h in range(hh):
			print("{} ".format(img[h][w])),
		print('\n')
	
if __name__ == '__main__':

	img = cv2.imread('src/output.jpg', 0)

	# first scan
	img_h, img_w = np.shape(img)
	label = 1
	new_img = [[0 for i in range(img_w)] for j in range(img_h)]
	

	for h in range(img_h):
		for w in range(img_w):
			if img[h][w] == 0:
				continue

			# judge left and top component
			if h > 0 and w > 0:

				l = new_img[h-1][w]
				r = new_img[h][w-1]
				

				if l==0 and r==0:
					new_img[h][w] = label

					label += 1
				elif l==0:
					new_img[h][w] = r
				elif r==0:
					new_img[h][w] = l
				else:
					# connected point        
					new_img[h][w] = min(l, r)
					union(l, r)
			
			elif h > 0:
				# left has no component
				l = new_img[h-1][w]
					
				if l != 0:
					new_img[h][w] = l
				else:
					new_img[h][w] = label
					label += 1
			elif w > 0:
				# up has no component
				
				l = new_img[h][w-1]
				if l != 0:
					new_img[h][w] = l
				else:
					new_img[h][w] = label
					label += 1
			else:
				new_img[h][w] = label
				label += 1
	
	#print_img(img, img_h, img_w)	
	# for i in range(50):
	# 	print(set1[i])
	color = {}
	max_label = -1
	# second sacn
	for w in range(img_w):
		for h in range(img_h):
			if new_img[h][w] != 0:
				r = find_parent( new_img[h][w] )
				new_img[h][w] = r
	
	t_img = np.zeros((img_h, img_w, 3), np.uint8)

	color_record = [[0, 0, 0] for i in range(999999)]
	# color_record = np.array(color_record)
	for h in range(img_h):
		for w in range(img_w):
			a = random.randint(0, 255)
			b = random.randint(0, 255)
			c = random.randint(0, 255)
			
			idx = new_img[h][w]
			idx = int(idx)
			if idx == 0:
				continue
			if color_record[idx] == [0, 0, 0]:
				color_record[idx] = [a, b, c]
			t_img[h][w] = color_record[idx]

	#print_img(t_img, img_h, img_w)	
	
	cv2.imshow('MyImage', t_img)
	cv2.imwrite("src/output2.jpg", t_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	
	
				

