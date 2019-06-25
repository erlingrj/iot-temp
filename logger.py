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

# For working with dates
import datetime
import dateutil.parser

# for enums
from enum import Enum
class LogEntryType(Enum):
    TEMP = 0
    CONTROL = 1

# For IO
from file_read_backwards import FileReadBackwards



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
        self.id = 1

        
        
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

        if topic == TOPICS['temp'][0] or topic == TOPICS['temp_setpoint'][0]:
            self.update_current_value_log(topic, payload_dict)

    def log_to_local_file(self, topic, payload_dict):
        # Open file
        fo = open(LOG_FILE_PATH, "a")
        # Write to the file
        fo.write(log_entry_encode(topic, payload_dict))
        # Close the file
        fo.close()
 
        


    def log_to_remote_db(self, topic, payload_dict):
        # Add the API key to the payload_dict
        payload_dict['APIKEY'] = APIKEY
        if topic == TOPICS['temp'][0]:
            try:
                r = requests.post(DB_POST_TEMP_PATH, json=payload_dict, headers = {'content-type': 'application/json'})
                if r.status_code != 200:
                    print("COULDNT POST: {}".format(r.text))
                else:
                    print(r.text)
            except Exception as e:
                print(e)
                print("No internet connection to log_to_remote_db")
        elif topic == TOPICS['temp_setpoint'][0]:
            try:
                r = requests.post(DB_POST_CONTROL_PATH, json=payload_dict, headers = {'content-type': 'application/json'})
                if r.status_code != 200:
                    print("COULDNT POST: {}".format(r.text))
                else:
                    print(r.text)
            except Exception as e:
                print(e)
                print("No internet connection to log_to_remote_db")

    def update_current_value_log(self, topic, payload_dict):
        print("JADDA")
        fo = open(CURRENT_STATE_PATH, "r")
        entry = fo.readlines()[0]
        fo.close()
        entry_dict = dict(item.split('=') for item in entry.split(';'))
        if topic == TOPICS['temp'][0]:
            entry_dict['TimestampTemp'] = payload_dict['Timestamp']
            entry_dict['Temp'] = payload_dict['Data']
        elif topic == TOPICS['temp_setpoint'][0]:
            entry_dict['TimestampControl'] = payload_dict['Timestamp']
            entry_dict['Control'] = payload_dict['Data']
        new_entry = ""
        for key,val in entry_dict.items():
            new_entry += "{}={};".format(key,val)
        new_entry = new_entry[:-1]
        print(new_entry)
        
        fo = open(CURRENT_STATE_PATH, "w")
        fo.write(new_entry)
        fo.close()


    
    async def poll_remote_db(self):
        # Poll last entry from DB
        try:
            r = requests.get(DB_GET_CONTROL_PATH, headers={'APIKEY':APIKEY})
            if r.status_code == 200:
                last_control = r.json()
                ret = compare_local_log(last_control, LogEntryType.CONTROL)

                if ret == -1:
                    print("Local log is outdated")
                    await self.publish_to(topic=TOPICS['temp_setpoint'][0],data=last_control['Data'])
                    # Update log file
                    self.log_to_local_file(TOPICS['temp_setpoint'][0], last_control)
                elif ret == 1:
                    print("remote DB is out-dated")
                    self.log_to_remote_db(topic=TOPICS['temp_setpoint'][0], payload_dict=read_log(LogEntryType.CONTROL, 1)[0])
                else:
                    print("Logger verify consistency between ")
            else:
                print("Failed to get control policy in poll_remote_db: {}".format(r.text))
        except:
            print("No internet connection to poll_remote_db")
            pass
        

        
    async def db_poller(self):
        # This is the infinte loop that keeps polling the DB
        while True:
            await self.poll_remote_db()
            await asyncio.sleep(10*60)
        

        
    
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
            self.loop.create_task(self.db_poller())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()


def log_entry_encode(topic, payload_dict):
    # Format the log entry
    if topic == TOPICS['temp'][0]:
        log_topic = LogEntryType.TEMP

    if topic == TOPICS['temp_setpoint'][0]:
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
    fo = FileReadBackwards(LOG_FILE_PATH, encoding="utf-8")
    entriesRead= 0

    entries = []
    for line in fo:
        entry_dict  = log_entry_decode(line)
        if int(entry_dict['EntryID']) == entryType.value:
            entriesRead += 1
            entries.append(entry_dict)
            if entriesRead == nEntries:
                break
    
    fo.close()
    return entries

def read_current_state_log():
    fo = open(CURRENT_STATE_PATH, "r")
    entry = fo.readlines()[0]
    fo.close()
    return dict(item.split('=') for item in entry.split(';'))



def compare_local_log(db_entry, entryType):
    last_local_entry = read_log(entryType, nEntries = 1)
    if not last_local_entry:
        return -1 # local out-of-date
    
    local_time = dateutil.parser.parse(last_local_entry[0]['Timestamp'])
    db_time = dateutil.parser.parse(db_entry['Timestamp'])

    if local_time > db_time:
        return 1
    elif db_time > local_time:
        return -1
    elif db_time == local_time:
        return 0
        

def get_temp_24h():
    # Construct the dates for the different intervals.
    resolution = 1
    n_hours = 24
    n_entries = n_hours * 3600 / TEMP_SAMPLING_INTERVAL
    now = datetime.datetime.now()
    h = datetime.timedelta(hours=1)
    now_rounded = now.replace(minute = 0, second=0, microsecond=0)
    dates = []
    # Construct the labels as datetime objects
    for i in range(int(n_hours/resolution),-1,-1):
        dates.append(now_rounded - i*h)
    dates.append(now.replace(microsecond = 0))

    # Get enough recent temp-entries
    entries = read_log(LogEntryType.TEMP, n_entries)
    values = create_stats_for_plotting(entries,dates)

    #Generate the strings for the plotting
    str_labels = [date.strftime("%a %H:%M") for date in dates[0:-1]]

    return (str_labels, values)
    
def create_stats_for_plotting(entries, dates):
    values = [None] * (len(dates)-1)
    tot = [0] * (len(dates)-1)
    n_vals = [0] * (len(dates)-1)

    for entry in entries:
        entry_time = dateutil.parser.parse(entry['Timestamp'])
        for idx, date in enumerate(dates):
            if idx == 0:
                if entry_time < date:
                    break
            elif idx == (len(dates)-2):
                tot[idx] += float(entry['Data'])
                n_vals[idx] += 1
            else:
                if entry_time < date:
                    tot[idx-1] += float(entry['Data'])
                    n_vals[idx-1] +=1
                    break
    
    for i, n_val in enumerate(n_vals):
        if n_val > 0:
            values[i] = tot[i]/n_val
    
    return values


def get_temp_1w():
    # Construct the dates for the different intervals.
    resolution=7
    n_hours = 24*7
    n_entries = n_hours * 3600 / TEMP_SAMPLING_INTERVAL
    now = datetime.datetime.now()
    h = datetime.timedelta(hours=resolution)
    now_rounded = now.replace(minute = 0, second=0, microsecond=0)
    dates = []
    # Construct the labels as datetime objects
    for i in range(int(n_hours/resolution),-1,-1):
        dates.append(now_rounded - i*h)
    dates.append(now.replace(microsecond = 0))
    # Get enough recent temp-entries
    entries = read_log(LogEntryType.TEMP, n_entries)
    values = create_stats_for_plotting(entries,dates)

    #Generate the strings for the plotting
    str_labels = [date.strftime("%-d/%m %H:%M") for date in dates[0:-1]]

    return (str_labels, values)

def get_current_control_policy():
    current_state = read_current_state_log()
    values = [float(x) for x in current_state['Control'].split('-')]
    labels = ["02:00", "04:00","06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "00:00"]
    return [labels, values]

def create_json(payload_dict):
    data  = {}
    data['APIKEY'] = APIKEY
    data['Timestamp'] = payload_dict['Timestamp']
    data['Data'] = payload_dict['Data']

    return json.dumps(data)



if __name__ == '__main__':
    MyLogger = Logger()
    MyLogger.run()
