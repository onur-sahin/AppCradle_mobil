import socket
import pickle
import struct
import cv2
import websockets
import asyncio

    # Business logic to receive data frames, and unpak it and de - serialize it and show video frame on client side


async def getVideo():
    
    payload_size = struct.calcsize("Q")

    URL = "ws://cradle-websocket-v3-2.herokuapp.com/"

    data = b""

    # Q: unsigned long long integer(8 bytes)


    async with websockets.connect(URL) as websocket:

        while True:
            print(124)
            while len(data) < payload_size:

    
                packet = await websocket.recv()
                
                if len(packet) > 0:
                    



        websocket.close()
    
if __name__ == "__main__":

    asyncio.run( getVideo() )
