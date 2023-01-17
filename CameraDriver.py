

import websockets
import asyncio
import json
import cv2
import struct
import imutils
import pickle
from math import ceil
from json import JSONEncoder
import numpy as np


class CameraDriver:

	URL = "wss://cradle-websocket-v3-2.herokuapp.com/"
	stop_signal = False

	video = False

	frame = None
	
	async def sendVideo(self):
		
		while True:
			
			try:
		
				async with websockets.connect(self.URL) as websocket:
					
					if self.video == True:
						vid = cv2.VideoCapture(0)
						
						# calculate a frame size
						
						img, self.frame = vid.read()
					
						self.frame = imutils.resize(self.frame, width=160)			
					
					self.stop_signal = False
					
					
					while(vid.isOpened()):

						img, self.frame = vid.read()
						frame = imutils.resize(frame,width=160)
						
						# print(np.size(frame))
						
				
						await websocket.send( pickle.dumps(frame, protocol=5) )  
						
						data = await websocket.recv()
						
						if len(data) < 1000:
							print(data)
						
						
						cv2.imshow('TRANSMITTING VIDEO', frame)
						
						if cv2.waitKey(1) & 0xFF == ord('q') :
							break
						
						if self.stop_signal == True:
							break
							
			except BaseException as err:
				print('Error  :' + str(err))
				
				
			if self.stop_signal == True:
				break
				
		websocket.close()
					
	def start_video_stream(self):
		asyncio.run( self.sendVideo() )


if __name__ == "__main__":
	
	cameraDriver = CameraDriver()
	cameraDriver.start_video_stream()
	
	

