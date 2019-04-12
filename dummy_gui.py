# Dummy GUI just printing date + current temp to the stdout
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio

# Just a variable used for conditional debugging prints
DEBUG = False


class GUI(MQTT_Client):
    def __init__(self):
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Define my_topic
        self.my_topic = [("TEMP", QOS_1)]
        # Subscribe to the topic. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topic))
    

    def packet_received_cb(self,packet):
        """
        THis function will be called each time a packet is received
        This should update a display box in 
        """
        topic = packet.variable_header.topic_name
        payload = packet.payload.data.decode('utf-8')
        if DEBUG:
            print("DEBUG: packet_received_cb called in dummy_gui")
            print("DEBUG: topic = {} payload = {}".format(topic,payload))
        
        # There will be several topics. So we should do a if-elif 
        # structure to handle the different incoming packets.
        if topic == "TEMP":
            # We wish to display on the screen
            # First split the packet into its format (btw these things will eventually be implemented in functions)
            day, month, year, hour, minute, sec, data = payload.split(':')
            print("TEMP = {}".format(data))
    
    def run(self):
        """
        This function starts the necessary tasks and runs them in the
        event loop. The GUI itself, probably implemented in TKinter should be
        added as a task here. 
        NB! The only code of importance here is the three first lines. The rest is a try to 
        shutdown the process properly when the user hits CTRL+C
        """
        try:
            self.loop.create_task(self.listen())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()

if __name__ == '__main__':
    GUI = GUI()
    GUI.run()