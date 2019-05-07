from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
from random import random
import asyncio
import datetime


class TempSensor(MQTT_Client):
    def __init__(self):
        MQTT_Client.__init__(self)
        self.current_temp = 0.0
        self.my_topic = ("TEMP", QOS_1)
        # The frequency of sampling the temperature
        self.sampling_period = 1

    async def main_loop(self):
        """
        The main loop is "modelling" the actual temperature sampling.
        Its a infinite while loop where it samples, publishes and then goes to sleep
        Currently it is just generating a random number.
        """
        while True:
            # GO to sleep and give CPU time to other tasks
            await asyncio.sleep(self.sampling_period)
            # Generate random new temperature
            self.current_temp = random()*30
            # Get current time
            t = datetime.datetime.now()
            # Make payload bytestring with timestamp
            payload = b'%d:%d:%d:%d:%d:%d:%f' %(t.day, t.month, t.year, t.hour, t.minute, t.second, self.current_temp)
            # Publish a new packet to the broker on topic stored in the class valye my_topic
            try:
                await self.publish_to(self.my_topic, payload)    
            except:
                pass

    def packet_received_cb(self,packet):
        """ This is the abstract method declared in the MQTT_Client class
            Here we implement what we wish when receiving a packet.
            Probably some switch-case statement on the topic of the packet
        """
        print(" %s => %s" % (packet.variable_header.topic_name, str(packet.payload.data)))


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


if __name__ == '__main__':
    T = TempSensor()
    T.run()
