# This is the first implementation of the socket client that the web service will run
# To connect to the RPi

import asyncio
from config import *
from random import random

class WebServiceClient():
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def tcp_client_loop(self):
        while True:
            next_msg = '{}'.format(random()*30)
            self.writer.write(next_msg.encode())
            await asyncio.sleep(2)

    
    async def tcp_client_setup(self):
        self.reader, self.writer = await asyncio.open_connection(WEBSERVICE_IP, WEBSERVICE_PORT)


    def run(self):
        self.loop.run_until_complete(self.tcp_client_setup())
        self.loop.create_task(self.tcp_client_loop())
        self.loop.run_forever()


if __name__ == '__main__':
    WS_client = WebServiceClient()
    WS_client.run()



            
