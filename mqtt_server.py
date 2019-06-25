
import logging
import asyncio
import os
from hbmqtt.broker import Broker

# Added by Erling. system-constants.py contains address and port
from config import *


# It is async meaning it can run concurrent with other thread in the process

async def broker_coro():
    # Initialize a new Broker with the config file
    broker = Broker(config = BROKER_CONFIG)
    # Yield from => run the function and wait until it returns
    await broker.start()

def run_broker():
    # Setting up logging to the terminal
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    # Asyncio is a Python lib for concurrent programming. I am not so familiar with the syntax and workings
    # But I believe it runs the broker_coro as a thread until completion (which should be never)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    # THen just loop forever. I dont think we ever reach this point in the code
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    run_broker()

