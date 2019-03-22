

import logging
import asyncio
import os
from hbmqtt.broker import Broker

# Added by Erling. system-constants.py contains address and port
from system_constants import *

broker_config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883',
            'max_connections': 10
        },
        'ws': {
            'type': 'ws',
            'bind': 'localhost:8080',
            'max_connections': 10
        },
    },
    'sys_interval': 0,
    'auth': {
        'allow-anonymous': True,
    }
}


@asyncio.coroutine
def broker_coro():
    broker = Broker(config = broker_config)
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    asyncio.get_event_loop().run_forever()

