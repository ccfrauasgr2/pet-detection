import requests
import json

class Network:
	def __init__(self, queue_lenght, url):
		self.queue_lenght = queue_lenght
		self.message_queue = list()
		self.url = url
	def debug(self, message):
		import json		
		with open('output/data2.json', 'w') as fp:
			fp.write(str(message))
			#json.dump(message, fp, indent=1)
		
	def sendPost(self, message, debug):
		if debug:
			self.debug(message)
		self.message_queue.append(message)
		if len(self.message_queue) == self.queue_lenght:			 
			#self._send()
			print("SEND")

	def _send(self):		
		try:
			if self.message_queue == 1:
				response = requests.post(self.url, data=message_queue[0])
			else:
				message={'message': json.dumps(message_queue)}
				response = requests.post(self.url, data=message)
			self.message_queue = list()
			response.raise_for_status() 
		except requests.exceptions.RequestException as e:
			print(f"RequestException: {e}")
			print(f"Status Code: {response.status_code}")
		except ValueError as e:
			print(f"ValueError: {e}")
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
