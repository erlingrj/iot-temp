# Implementation of the web-service client

from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio
import tkinter as Tk

from config import *
from packet import *
# Just a variable used for conditional debugging prints
DEBUG = False




class WebServiceServer(MQTT_Client):
    def __init__(self):
        # Init the MQTT_Client
        MQTT_Client.__init__(self)

    def client_connected_cb(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.loop.create_task(self.tcp_server_loop())
    
    async def tcp_server_loop(self):
        while True:
            data = await self.reader.read(100)
            print(f'Received: {data.decode()!r}')
            # If statements selecting the correct action from here
            # Probably involves publishing it to a topic
        

    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received
        the WebServiceClient should never receive a packet
        """
        raise Exception(1)

    def run(self):
        """
        This function starts the necessary tasks and runs them in the
        event loop. The GUI itself, probably implemented in TKinter should be
        added as a task here. 
        NB! The only code of importance here is the three first lines. The rest is a try to 
        shutdown the process properly when the user hits CTRL+C
        """

        # Setup connection
        self.loop.run_until_complete(asyncio.start_server(self.client_connected_cb, 'localhost', 8888, loop=self.loop)) 
        print("Socket sucessfully created")
        

        try:
            # Spawn the tasks to run concurrently
            self.loop.create_task(self.listen()) # Listen to subscribed topics
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()


if __name__ == '__main__':
    WS_server = WebServiceServer()
    WS_server.run()
