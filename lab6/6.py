import tello
import cv2
from tello_control_ui import TelloUI
import time

import numpy as np


def main():
	drone = tello.Tello('', 8889)

	time.sleep(5)
	fs = cv2.FileStorage("data.txt", cv2.FILE_STORAGE_READ)
	cameraMatrix = fs.getNode("intrinsic")
	distCoeffs = fs.getNode("distortion")
	cameraMatrix = cameraMatrix.mat()
	distCoeffs = distCoeffs.mat()
	dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
	parameters =  cv2.aruco.DetectorParameters_create()
	while(1):
		frame = drone.read() 
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

		############
		
		markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
		frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
		rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 13.7, cameraMatrix, distCoeffs) 
		# print(tvec)
		# print(rvec)
		t_vec = tvec[0][0]
		# string = str(", ".join(tvec[0]))
		try:
			string = "x: " + str(round(t_vec[0], 3)) + ", " + "y: " + str( round(t_vec[1], 3)) + " z: " +  ", " + str( round(t_vec[2], 3))
			cv2.putText(frame, string , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA )
			frame = cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 10)
			
			# get rotation matrix
			rtm = cv2.Rodrigues(rvec)
			z = [0, 0, 1]
			# dot product of two vec
			v_ = -np.dot(np.array(rtm[0]), np.array(z))

			# project to xz plane
			v[1] = 0

			radis = math.atan2(v[0], v[2])
			angle = math.degrees(radis)
			distance = 0.3

			if np.abs(angle/2.0) > 20:
				if angle > 0:
					drone.rotate_cw(np.abs(angle/3))
				else:
					drone.rotate_ccw(np.abs(angle/3))
			else:
				if t_vec[2] < 70:
					drone.move_backward(distance)
				else:	
					drone.move_forward(distance)

			# adjust direction
			# # x > 0, move right
			# if t_vec[0] > 0.3: 
			# 	drone.move_right(distance)
			# # x < 0, move left
			# if t_vec[0] < -0.3:
			# 	drone.move_left(distance)
			# # y > 0, move down
			# if t_vec[1] > 0.3:
			# 	drone.move_down(distance)
			# # y < 0, move up
			# if t_vec[1] < -0.3:
			# 	drone.move_up(distance) 
			# z > 0, move front
			# if t_vec[2] > 0.8:
			# 	drone.move_forward(distance)
			# if t_vec[2] < 0.8:
			# 	drone.move_backward(distance)
			
			
		except:
			pass
		finally:
			cv2.imshow("frame",frame)
			key = cv2.waitKey(32)

			if key!= -1:
				drone.keyboard(key)


if __name__ == "__main__":
	main()
