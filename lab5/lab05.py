import tello
import cv2
from tello_control_ui import TelloUI
import time

def main():
	drone = tello.Tello('', 8889)

	time.sleep(5)
	fs = cv2.FileStorage("data.txt", cv2.FILE_STORAGE_READ)
	cameraMatrix = fs.getNode("intrinsic")
	distCoeffs = fs.getNode("distortion")
	cameraMatrix = cameraMatrix.mat()
	distCoeffs = distCoeffs.mat()

	while(1):
		frame = drone.read() 
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

		############
		dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
		parameters =  cv2.aruco.DetectorParameters_create()
		markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
		frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
		rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 13.7, cameraMatrix, distCoeffs) 
		print(tvec)
		# string = str(", ".join(tvec[0]))
		try:
			string = "x: " + str(round(tvec[0][0][0], 3)) + ", " + "y: " + str( round(tvec[0][0][1], 3)) + " z: " +  ", " + str( round(tvec[0][0][2], 3))
			cv2.putText(frame, string , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA )
			frame = cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 10)
		except:
			pass
		finally:
			cv2.imshow("frame",frame)
			key = cv2.waitKey(1)

			if key!= -1:
				drone.keyboard(key)


if __name__ == "__main__":
    main()
