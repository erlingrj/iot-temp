# Setting up a client that subscribes to the topic MYTOPIC and prints the messages it receives
# It runs forever so you need to exit it with Ctrl-C

import asyncio

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2


@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    # Connect address, protocol and port must match what the broker is set for. See mqtt-server.py
    yield from C.connect('ws://localhost:8080/')
    # Subscribe to MYTOPIC
    yield from C.subscribe([
            ('MYTOPIC', QOS_1)]) # We must also specify the Quality Of Service (i.e. if there is reliable delivery with ACKs and so on)
    print("subscibed!")
    i=0
    while True:
        i+=1
        # Wait until you receive a message from the broker
        m = yield from C.deliver_message()
        print("RECEIVED PACKET: {}".format(m))
        # Format packet
        packet = m.publish_packet
        #Print
        print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
  
