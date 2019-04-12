
# This is a basic implementation of the MQTT Broker. This will soon be replaced by a proper object oriented implementation

import logging
import asyncio
import os
from hbmqtt.broker import Broker

# Added by Erling. system-constants.py contains address and port
from system_constants import *

# THis is the default config of the Broker
broker_config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883',
            'max_connections': 10
        },
        'ws': {
            'type': 'ws',
            'bind': 'localhost:8080', # THis must match the connectin Clients
            'max_connections': 10
        },
    },
    'sys_interval': 0,
    'auth': {
        'allow-anonymous': True
    },
    'plugins' : ['auth_anonymous'],
    'topic-check' : {
        'enabled' : True,
        'plugins' : ['topic_taboo'], #This is important for allowing subscribing to random topics
    },
}

# It is async meaning it can run concurrent with other thread in the process

async def broker_coro():
    # Initialize a new Broker with the config file
    broker = Broker(config = broker_config)
    # Yield from => run the function and wait until it returns
    await broker.start()


if __name__ == '__main__':
    # Setting up logging to the terminal
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    # Asyncio is a Python lib for concurrent programming. I am not so familiar with the syntax and workings
    # But I believe it runs the broker_coro as a thread until completion (which should be never)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    # THen just loop forever. I dont think we ever reach this point in the code
    asyncio.get_event_loop().run_forever()

