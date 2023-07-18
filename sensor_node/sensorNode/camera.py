from picamera2 import Picamera2
import cv2
import time

class Camera:
	def __init__(self):
		self.camera = Picamera2()
		#self.config = self.camera.create_still_configuration({"size":(640,480)})
		self.camera.start()
		
	def take_image(self):
		return self.camera.capture_image()
	
	def take_array(self):
		return self.camera.capture_array()
		
	def stop_camera(self):
		self.camera.stop()
