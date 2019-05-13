# The logger subscribes to various topics and creates a local and remote log
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio

# Configuration of TOPICS and addresses
from config import *

# For exception handeling
import sys


# Just a variable used for conditional debugging prints
DEBUG = False

class Logger(MQTT_Client):
    def __init__(self): 
        # Setup the MQTT stuff from parent
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Store what topics to listen to
        self.my_topics = [TOPICS['temp'], TOPICS['temp_setpoint'], TOPICS['ping']]
        # Subscribe to the topics. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topics))
        
        
    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received. Make an entry in local and remote log
        """
        if DEBUG:
            print("DEBUG: packet_received_cb called in dummy_gui")
            print("DEBUG: topic = {} data = {}".format(topic, payload_dict['data']))
        
        # There will be several topics. So we should do a if-elif 
        # structure to handle the different incoming packets.
        # We wish to display on the screen
        # First split the packet into its format (btw these things will eventually be implemented in functions)
        data = payload_dict['data']
        self.current_temp.set(data)


    
    def run(self):
        """
        This function starts the necessary tasks and runs them in the
        event loop. The GUI itself, probably implemented in TKinter should be
        added as a task here. 
        NB! The only code of importance here is the three first lines. The rest is a try to 
        shutdown the process properly when the user hits CTRL+C
        """
        try:
            # Spawn the tasks to run concurrently
            self.loop.create_task(self.listen()) # Listen to subscribed topics
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()




if __name__ == '__main__':
    MyLogger = Logger()
    MyLogger.run()
