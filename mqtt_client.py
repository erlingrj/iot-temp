#!/usr/python3

# This is the abstract base class for the MQTT-Clients
# As of this point, it doesn't implement any error checking on 
# The connection etc. should be expanded to include this later
from abc import ABC, abstractmethod

import asyncio
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


class MQTT_Client(ABC):
    def __init__(self):
        """
        Initializing the client
        """
        # The broker addressed should be passed in a more intelligent way
        self.broker_addr = 'ws://localhost:8080/'
        # Initializing a new client object
        self.C = MQTTClient()
        # getting the asyncio event loop
        self.loop = asyncio.get_event_loop()
        # Run the set-up to completion before moving on
        self.loop.run_until_complete(self.setup())


    async def setup(self):
        # Connect to a MQTT broker
        await self.C.connect(self.broker_addr)

    async def subscribe_to(self,topic_array):
        """
        topic_array = [(topic1, QOS), (topic2, QOS)] an array of tuples
        """
        # Subscribes to the topic and calls the callback when it receives
        # A packet on that topic
        # It will run in an infinite loop

        await self.C.subscribe(topic_array)
        print("SUBSCRIBED to topic: {} QOS: {}".format(topic_array[0][0], topic_array[0][1]))

    async def unsubscribe_from(self, topic_array):
        # This function allows us to unsubscribe from the topics in topic_array
        # NOT USED SO FAR
        pass
    
    async def publish_to(self,topic, payload):
        # Publishes to the topic
        await self.C.publish(topic[0],payload)
        print("Packet successfully published") 

    async def listen(self):
        # Is running in an infinite loop listening on receiving packets
        while True:
            p = await self.C.deliver_message()
            try:
                p_format = p.publish_packet
                # Call the abstract callback function that the child will implement
                self.packet_received_cb(p_format)
            except:
                pass

    @abstractmethod
    def packet_received_cb(self, packet):
        """
        This callback function is called each time the client
        receives a packet on a topic it is subscribing to
        THe function has to be implemented in all children of this class
        """
        pass
