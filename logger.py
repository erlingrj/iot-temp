# The logger subscribes to various topics and creates a local and remote log
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio

# Configuration of TOPICS and addresses
from config import *

# For exception handeling
import sys


# Just a variable used for conditional debugging prints
DEBUG = True

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
        self.log_to_local_file(topic, payload_dict)

        self.log_to_remote_db(topic, payload_dict)

    def log_to_local_file(self, topic, payload_dict):
        # Open file
        fo = open(LOG_FILE_PATH, "a")
        # Write to the file
        fo.write("Timestamp:{}-{}-{}-{}-{}-{} Topic:{} Data:{}\n".format(
            payload_dict['day'],payload_dict['month'],payload_dict['year'],payload_dict['hour'],payload_dict['min'],payload_dict['sec'],topic, payload_dict['data']
            ))
        # Close the file
        fo.close()

        


    def log_to_remote_db(self, topic, payload_dict):
        print("log to remote is yet to be implemented")
        raise(Exception)


    
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


def log_entry_encode(topic, payload_dict):
    # Format the log entry
    print("Not yet implemented")
    raise()

def log_entry_decode(entry):
    # Take a log entry and return the topic and payload_dict
    print("Not yet implemented")
    raise()

if __name__ == '__main__':
    MyLogger = Logger()
    MyLogger.run()
