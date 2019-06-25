# Dummy GUI just printing date + current temp to the stdout
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio
import tkinter as Tk

from config import *
from packet import *
# Just a variable used for conditional debugging prints
DEBUG = False


class TempController(MQTT_Client):
    def __init__(self): 
        # Setup the MQTT stuff from parent
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Define my_topic
        self.my_topic = [TOPICS['temp_setpoint'], TOPICS['temp']]
        # Subscribe to the topic. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topic))

        self.current_setpoint = 0.0
        self.id = 4
        
        
    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received
        This should update a display box in 
        """
        data = payload_dict['Data']
        self.current_setpoint = data
         
        if DEBUG:
            print("New dummy_temp_controller setpoint = {}".format(self.current_setpoint))
        

  
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

def run():
    TC = TempController()
    TC.run()

if __name__ == '__main__':
    run()
