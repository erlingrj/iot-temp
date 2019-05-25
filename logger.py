# The logger subscribes to various topics and creates a local and remote log
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio

# For making GET/POST request to WEB
import requests

# For structuring data
import json

# Configuration of TOPICS and addresses
from config import *

# For exception handeling
import sys

# for enums
from enum import Enum
class LogEntryType(Enum):
    TEMP = 0
    CONTROL = 1



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
            print("DEBUG: packet_received_cb called in logger.py")
            print("DEBUG: topic = {} data = {}".format(topic, payload_dict['Data']))
        
        # There will be several topics. So we should do a if-elif 
        # structure to handle the different incoming packets.
        self.log_to_local_file(topic, payload_dict)

        self.log_to_remote_db(topic, payload_dict)

    def log_to_local_file(self, topic, payload_dict):
        # Open file
        fo = open(LOG_FILE_PATH, "a")
        # Write to the file
        fo.write(log_entry_encode(topic, payload_dict))
        # Close the file
        fo.close()
 
        


    def log_to_remote_db(self, topic, payload_dict):
        print("log to remote")
        # Add the API key to the payload_dict
        payload_dict['APIKEY'] = APIKEY
        print(payload_dict)
        if topic == TOPICS['temp'][0]:
            r = requests.post(DB_POST_TEMP_PATH, json=payload_dict, headers = {'content-type': 'application/json'})
            if r.status_code != 200:
                print("COULDNT POST: {}".format(r.text))
            else:
                print(r.text)
            
        elif topic == TOPICS['temp_setpoint'][0]:
            r = requests.post(DB_POST_CONTROL_PATH, data=payload_dict)
            if r.status_code != 200:
                print("COULDNT POST: {}".format(r.text))
            else:
                print(r.text)
    
    def poll_remote_db(self):
        # Poll last entry from DB
        r = requests.get(DB_GET_TEMP_PATH)
        if r.status_code == 200:
            last_temp = r.json()
            ret = compare_local_log(last_temp, LogEntryType.TEMP)
            if ret == -1:
                # Log is out-of-date
                print("This should be impossible!")
                # Send on MQTT
                self.publish_to(topic=LogEntryType.TEMP,data=last_temp['Data'])
                # Update log file
                self.log_to_local_file(topic=LogEntryType.TEMP,payload_dict=last_temp)

            if ret == 1:
                # Remote db is out-of-date
                print("DB is not updated on last temp")
                self.log_to_remote_db(topic=LogEntryType.TEMP, payload_dict=read_log(LogEntryType.TEMP, 1)[0])
                

        else:
            print(r.text)
        

        r = requests.get(DB_GET_CONTROL_PATH)
        if r.status_code == 200:
            last_control = r.json()
            print(last_control)
            ret = compare_local_log(last_control, LogEntryType.CONTROL)
            if ret == -1:
                # Log is out-of-date
                print("This should be impossible!")
                # Send on MQTT
                self.publish_to(topic=LogEntryType.CONTROL,data=last_control['Data'])
                # Update log file
                self.log_to_local_file(topic=LogEntryType.CONTROL,payload_dict=last_control)

            if ret == 1:
                # Remote db is out-of-date
                print("DB is not updated on last temp")
                self.log_to_remote_db(topic=LogEntryType.TEMP, payload_dict=read_log(LogEntryType.TEMP, 1)[0])
        else:
            print(r.text)

        
    async def db_poller(self):
        # This is the infinte loop that keeps polling the DB
        while True:
            self.poll_remote_db()
            await asyncio.sleep(10)
        

        
    
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
            #self.loop.create_task(self.db_poller())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()


def log_entry_encode(topic, payload_dict):
    # Format the log entry
    if topic == TOPICS['temp'][0]:
        log_topic = LogEntryType.TEMP

    if topic == TOPICS['temp_setpoint']:
        log_topic = LogEntryType.CONTROL

    logEntry = "EntryID={};Timestamp={};Data={}\n".format(
            log_topic.value, payload_dict['Timestamp'], payload_dict['Data']
    )
    return logEntry
    

def log_entry_decode(entry):
    # Take a log entry and return the topic and payload_dict
    my_dict = dict(item.split('=') for item in entry.split(';'))

    return my_dict


# Main entry point to reading the log
def read_log(entryType, nEntries):
    fo = open(LOG_FILE_PATH, "r")
    entriesRead= 0

    entries = []
    for line in fo:
        entry_dict  = log_entry_decode(line)
        if entry_dict['EntryID'] == entryType:
            entriesRead += 1
            entries.append(entry_dict)
    
    fo.close()
    return entries


def compare_local_log(db_entry, entryType):
    last_local_entry = read_log(entryType, nEntries = 1)
    if not last_local_entry:
        return -1 # local out-of-date
    
    if last_local_entry[0]['Timestamp'] != db_entry['Timestamp']:
        local_time = last_local_entry[0]['Timestamp'].split('-')
        db_time = db_entry['Timestamp'].split('-')
        for i in [2,1,0,3,4,5]:
            if local_time[i] > db_time[i]:
                return 1 # DB is out-of-date
            if db_time[i] > local_time[i]:
                return -1
        
    return 0




def get_temp_24h():
    print("To be implemented")
    # return 

def get_temp_1w():
    print("To be implemented")
    # Return

def get_current_control_policy():
    return read_log(entryType = LogEntryType.CONTROL, nEntries = 1)

def create_json(payload_dict):
    data  = {}
    data['APIKEY'] = APIKEY
    data['Timestamp'] = payload_dict['Timestamp']
    data['Data'] = payload_dict['Data']

    return json.dumps(data)



if __name__ == '__main__':
    MyLogger = Logger()
    MyLogger.run()
