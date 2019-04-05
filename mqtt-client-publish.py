# This script publishes three messages to the topic MYTOPIC and then exits

import asyncio

from hbmqtt.client import MQTTClient

# Again, this is a async co-routine that can run together with other threads (like a UI or anything)
@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    # must match what we specified in the broker
    yield from C.connect('ws://localhost:8080/')
    # Publish the three packets
    message = yield from C.publish('MYTOPIC', b'This is message number 1')
    message1 = yield from C.publish('MYTOPIC', b'And here come number 2')
    message2 = yield from C.publish('MYTOPIC', b'Atlast, number 3 as well')
    print("messages published\n Good Bye!")


            
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test_coro())