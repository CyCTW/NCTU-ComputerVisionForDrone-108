import cv2
import numpy as np
import math


warp_coord = np.empty([4, 2], dtype="float32")
idx = 0
# click four coordinate add picture
str = ["Upper-left corner", "Lower-left corner", "Lower-right corner", "Upper-right corner"]
def callback(event, x, y, flags, param):
	global idx
	if event == cv2.EVENT_LBUTTONDOWN:
		warp_coord[idx] = [x, y]
		print(str[idx] + " is "),
		print(x, y)
		idx += 1
		if idx <= 3:
			print("Please Click " + str[idx])
		else:
			print("Press any key to continue")
img = cv2.imread('src/warp.jpg', 1)
cv2.namedWindow("ClickCoordinate")
cv2.setMouseCallback("ClickCoordinate", callback)

cv2.imshow("ClickCoordinate", img)
print("Please Click " + str[idx])
	
key = cv2.waitKey(0)
cv2.destroyAllWindows()

#########################################################
cap = cv2.VideoCapture(0) # device

img_warp = cv2.imread('src/warp.jpg')

while True :
	ret, frame = cap.read()
	
	# find corner points
	if ret == True:
		h, w = frame.shape[:2]
		origin_coord = np.array( [ [0., 0.], [0., h], [w, h], [w, 0.]], dtype="float32")

		M = cv2.getPerspectiveTransform(origin_coord, warp_coord)
		dst = cv2.warpPerspective(frame, M, (w, h), cv2.INTER_LINEAR)
		w_coord = warp_coord.astype('int32')
		
		cv2.fillConvexPoly(img_warp, w_coord, (0, 0, 0))
		
		dst = cv2.add(img_warp, dst)
		cv2.imshow("test", dst)
		
		key = cv2.waitKey(30) & 0XFF
		if key != 255:
			break
