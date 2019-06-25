from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
from random import random
import asyncio
import datetime

from w1thermsensor import W1ThermSensor
from config import *


class TempSensor(MQTT_Client):
    def __init__(self):
        MQTT_Client.__init__(self)
        self.sensor = W1ThermSensor()
        self.current_temp = 0.0
        # self.my_topic = ("TEMP", QOS_1)
        self.my_topic = TOPICS['temp']
        # The frequency of sampling the temperature
        self.sampling_period = 3*60
        self.id = 3

    async def main_loop(self):
        """
        The main loop is "modelling" the actual temperature sampling.
        Its a infinite while loop where it samples, publishes and then goes to sleep
        Currently it is just generating a random number.
        """
        while True:
            # Generate random new temperature
            self.current_temp = self.sensor.get_temperature()
            # Publish the new tempe
            await self.publish_to(self.my_topic[0], self.current_temp)
             # GO to sleep and give CPU time to other tasks
            await asyncio.sleep(SENSOR_SAMPLING_INTERVAL_S)

            

    def packet_received_cb(self,topic, payload_dict):
        """ This is the abstract method declared in the MQTT_Client class
            Here we implement what we wish when receiving a packet.
            Probably some switch-case statement on the topic of the packet
        """
        print("ERROR TEMP SENSOR RECEIVES NO PACKETS")


    def run(self):
        """
        This is the procedure that runs the TempSensor object
        Sets up the tasks and starts the event loop.
        NB! The only code of importance here is the three first lines. The rest is a try to 
        shutdown the process properly when the user hits CTRL+C
        """
        try:
            self.loop.create_task(self.listen())
            self.loop.create_task(self.main_loop())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()

def run():
    T = TempSensor()
    T.run()

if __name__ == '__main__':
    run()

