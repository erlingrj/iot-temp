# Dummy GUI just printing date + current temp to the stdout
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio
import tkinter as Tk

# Configuration of TOPICS and addresses
from config import *

# For exception handeling
import sys


# Just a variable used for conditional debugging prints
DEBUG = False


class GUI(MQTT_Client):
    def __init__(self): 
        # Setup the MQTT stuff from parent
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Define my_topic
        #self.my_topic = [("TEMP", QOS_1)]
        self.my_topic = [TOPICS['temp']]
        # Subscribe to the topic. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topic))
        
        
    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received
        This should update a display box in 
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

    # Functions for handeling button-events
    def tkinter_set_temperature_button_pressed(self):
        # Send the setpoint

        #First create a bytestring to send
        payload = b'%f' % float(self.temp_setpoint.get())
        
        # The we call the async function publish_to with the right topic
        # We use ensure_future as it is an async function and we cannot call await on it
        # since we are inside a non-async function
        asyncio.ensure_future( self.publish_to(TOPICS['temp_setpoint'], payload) )

        print("Set temperature button pressed\nSetpoint = {}".format(self.temp_setpoint.get()))
        

    def tkinter_setup(self):
         # Setup the TK GUI
        self.root = Tk.Tk()
        self.current_temp = Tk.StringVar() #Textvariable for updating the label
        self.temp_setpoint = Tk.StringVar()
        self.label_temp = Tk.Label(self.root, textvariable=self.current_temp)
        self.label_temp.grid(row = 0, column = 1)
        self.label_description = Tk.Label(self.root, text = "Current Temperature: ")
        self.label_description.grid(row = 0, column = 0)

        self.button = Tk.Button(self.root, text="Set Temperature", command=self.tkinter_set_temperature_button_pressed)
        self.entry_temp = Tk.Entry(self.root, textvariable=self.temp_setpoint)
        self.entry_temp.grid(row=1, column=0)
        self.button.grid(row=1, column=1)
        self.tk_interval = 0.001
    
    def run(self):
        """
        This function starts the necessary tasks and runs them in the
        event loop. The GUI itself, probably implemented in TKinter should be
        added as a task here. 
        NB! The only code of importance here is the three first lines. The rest is a try to 
        shutdown the process properly when the user hits CTRL+C
        """

        # Setup TKinter
        self.tkinter_setup()
        try:
            # Spawn the tasks to run concurrently
            self.loop.create_task(self.listen()) # Listen to subscribed topics
            self.loop.create_task(self.run_tk()) # Run GUI
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()


    async def run_tk(self):
        """
        Run TK with asyncio
        """
        while True:
            self.root.update()
            self.root.update_idletasks()
            await asyncio.sleep(self.tk_interval) #tk_interval is defined in the __init__
        
        


if __name__ == '__main__':
    GUI = GUI()
    GUI.run()
