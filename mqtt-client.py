# THis is copied and pasted from hbmqtt documentation

import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

from system_constants import *

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    # Connect address, protocol and port must match what the broker is set
    # up for.
    yield from C.connect('ws://localhost:8080/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    # Subscribe to '$SYS/broker/load/#' with QOS=2

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())

