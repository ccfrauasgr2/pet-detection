#https://docs.ultralytics.com/modes/predict/#probs
from ultralytics import YOLO
from PIL import Image
import cv2

class NoBoundingBoxDetected(Exception):
	'Used whene there are no Boundingbox in results' 
	pass

class Detection:
	def __init__(self, model_path, conf):
		self.model = YOLO(model_path)
		self.conf = conf
			
	def make_prediction(self, input):
		results = self.model.predict(source=input, save=False, conf=self.conf)
		if not results[0].boxes:
			raise NoBoundingBoxDetected()			
		return results
	
	def make_plot(self, results):
		if results[0].boxes:
			return results[0].plot()
		else:
			raise NoBoundingBoxDetected()
