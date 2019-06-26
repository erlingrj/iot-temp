# Dummy GUI just printing date + current temp to the stdout
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio
import tkinter as Tk

from config import *
from packet import *

from datetime import datetime

import logger
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

        self.current_control_policy = logger.get_current_control_policy()
        self.current_temp = logger.get_current_temp()
        self.current_hour = datetime.now().hour
        
        self.id = 4
        
        
    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received
        This should update a display box in 
        """
        data = payload_dict['Data']
        if (topic == TOPICS['temp'][0]):
            self.current_temp = float(data)
        elif (topic == TOPICS['temp_setpoint'][0]):
            self.current_control_policy = [float(x) for x in data.split('-')]

        asyncio.ensure_future(self.evaulate_control())

                
    async def controller_loop(self):
        while True:
            await self.evaluate_control()
            await asyncio.sleep(CONTROLLER_SAMPLING_INTERVAL_S)
        
        
        

  
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
            self.loop.create_task(self.controller_loop())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()

    
    def make_controller_payload(self):
        return "{{Heater:{},AC:{}}}".format(self.heater, self.ac)
    
    async def  evaluate_control(self):
        self.current_hour = datetime.now().hour
        if (self.current_temp > self.current_control_policy[1][hour_to_policy_index(self.current_hour)]):
            self.ac = "ON"
            self.heater = "OFF"
        elif (self.current_temp <  self.current_control_policy[1][hour_to_policy_index(self.current_hour)]):
            self.ac = "OFF"
            self.heater = "ON"
        else:
            self.ac = "OFF"
            self.heater = "OFF"

        await self.publish_to(TOPICS['controller'][0], self.make_controller_payload())




def run():
    TC = TempController()
    TC.run()

def hour_to_policy_index(hour):
    if (hour < 2):
        return 11
    hour -=  2
    return int(hour/2)

if __name__ == '__main__':
    run()
