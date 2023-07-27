import json
import cv2
import numpy as np
from compress import Compress

LABEL = {'cat':0, 'dog':1}
class Package:
	def __init__(self,image, date, time, detections):
		self.image = image
		self.date = date
		self.time = time
		self.detections = detections
		
		
	def _makeObject(self, detected_type, acc, bid):
		return {
			'type': detected_type,
			'accuracy': acc.tolist(),
			'bid': bid
			}
			
	def _getType(self, cls):
		if int(cls.tolist()) == LABEL['cat']:								
			detected_type='Cat'
		elif int(cls.tolist()) == LABEL['dog']:							
			detected_type = 'Dog'
		else:
			raise ValueError(f"Label has wrong ID: {cls}")	
		return detected_type
			
	def _getOutput(self, detections):
		c = Compress()
		self.image = c.compress_jpg(self.image)		
		return {
		'picture': c.toBase64(),
		'date': self.date,
		'time': self.time,
		'detections': detections	
		}		
	
	def _makePlot(self, image, bounding_boxes, detections):
		image_with_boxes = np.copy(image)
		for box, item in zip(bounding_boxes, detections):
			label=item['type']
			bid=str(item['bid'])
			x1, y1, x2, y2 = map(int, box)
			cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
			label_text = label+bid
			(label_width, label_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
			cv2.rectangle(image_with_boxes, (x1, y1 - label_height), (x1 + label_width, y1), (0, 255, 0), cv2.FILLED)
			cv2.putText(image_with_boxes, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
			
		self.image = image_with_boxes		
		
	def toJson(self):
		detections = list()
		detected_type = list()
		bid=1
		for acc,cls in zip(self.detections[0].boxes.conf, self.detections[0].boxes.cls):
			detected_type.append(self._getType(cls))
			detected_object=self._makeObject(detected_type[-1], acc, bid )
			detections.append(detected_object)
			bid+=1
				
		self._makePlot(self.image, self.detections[0].boxes.xyxy, detections)
		return json.dumps(self._getOutput(detections), indent=1)
