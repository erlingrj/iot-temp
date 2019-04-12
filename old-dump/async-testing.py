# This is script that I will use for testing how to do concurrent single-threaded programming with async.
# The challenge is to run the HBMQTT client together with other tasks like checking temperature or running a GUI.


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
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(uptime_coro())
    main_loop.run_until_complete(another_function())
    
    print("hallo")