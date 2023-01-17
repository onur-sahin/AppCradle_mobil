import socket
import pickle
import struct
import cv2
import websockets
import asyncio
import threading
from time import sleep
import imutils

    # Business logic to receive data frames, and unpak it and de - serialize it and show video frame on client side


class CameraDriver:

    frame = cv2.imread('./images/loading.png')

    async def getVideo(self, *args):
        
        URL = "ws://cradle-websocket-v3-2.herokuapp.com/"

        ping_data = pickle.dumps('ping', protocol=5)

        restart = False
        self.stop_signal = False

        

        # Q: unsigned long long integer(8 bytes)

        while True:
            restart = False
            async with websockets.connect(URL) as websocket:

                print("connected to \'ws://cradle-websocket-v3-2.herokuapp.com/\'")

                while True:

                    try:
                        await websocket.send(ping_data)
                        print("sent ping")
                    
                    except BaseException as err:
                        print('Error in \'await websocket.send(pickle.dumps(\'ping\', protocol=5))\'  :' + str(err))
                        restart = True
                        break

                    for i in range(100):
                        sleep(0.01)

                        try:
                            packet = await websocket.recv()
                            print("bura")

                            if len(packet) < 10000 :
                            
                                print(packet)

                            else:

                                # de - serialize bytes into actual frame type
                                
                                self.frame = pickle.loads(packet)
                                # self.frame = imutils.resize(self.frame, width=320)
                                # print(len(self.frame))
                                # show video frame at client side
                            
                                # cv2.imshow("RECEIVING VIDEO", self.frame)

                            key = cv2.waitKey(1) & 0xFF
                            

                            if key == ord('q') or self.stop_signal == True:                                 # press q to exit video
                                self.stop_signal = True
                                break



                        except BaseException as err:
                            print('Error in \'for i in range(20): \':  ' + str(err))
                            restart = True
                            break

                    if self.stop_signal == True or restart == True:
                        break

            if self.stop_signal == True:
                break
        
        websocket.close()
        self.frame = cv2.imread('./images/loading.png')
        print("disconnected from \'ws://cradle-websocket-v3-2.herokuapp.com/\'")

    def start_receiving_video(self):
        asyncio.run( self.getVideo() )
    
if __name__ == "__main__":
    cameraDriver = CameraDriver()
    cameraDriver.start_receiving_video()
