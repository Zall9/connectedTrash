from picamera2 import Picamera2, Preview

import time

class Camera:
	def __init__(self):
		self.camera = Picamera2()
		self.camera_config = self.camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
		self.camera.configure(self.camera_config)

	
	def screenshot(self, input="./image.jpg"):
		self.camera.start()
		time.sleep(1)
		self.camera.capture_file(input)
		self.camera.stop_recording()
		
