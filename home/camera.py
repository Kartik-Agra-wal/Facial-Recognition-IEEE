import cv2
from django.conf import settings

haar_cascade = cv2.CascadeClassifier('D:\\My files\\Django projects\\Facial Recognition app\\facial_recog\\home\\haar_face.xml')

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		_, image = self.video.read()

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()