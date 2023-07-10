from PIL import Image
import zlib
import cv2
import base64
import sys

import numpy as np
class Compress:
	last_img_path = None		
	def _convert(self, img_format, image, temp_input, temp_output):
		cv2.imwrite(temp_input,image)
		image = Image.open(temp_input)
		image.save(temp_output, img_format, optimize = True, quality = 90)
		self.last_img_path = temp_output
		return np.asarray(Image.open(temp_output)) 		
	
	def compress_jpg(self, image):
		temp_input_path = "/dev/shm/input.JPG"
		temp_output_path = "/dev/shm/output.JPG"
		return self._convert("JPEG", image, temp_input_path, temp_output_path)
		
		
	def compress_png(self, image):
		temp_input_path = "/dev/shm/input.PNG"
		temp_output_path = "/dev/shm/output.PNG"
		cv2.imwrite(temp_input_path,image)
		return self._convert("PNG", image, temp_input_path, temp_output_path)
		
	def compress_zip(data):		
		data =	zlib.compress(data.encode())			
		return data
		
	def toBase64(self):
		with open(self.last_img_path , 'rb') as f:
			return base64.b64encode(f.read()).decode('utf-8')
