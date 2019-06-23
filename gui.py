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
DEBUG = True


import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


LARGE_FONT = ("Verdana", 24)
MENU_BUTTON_HEIGHT = 2
MENU_BUTTON_COLOR = 'green'
MENU_BUTTON_WIDTH = 15
MENU_BUTTON_FONT = ("Verdana", 22)
RPI_HEIGHT = 400
RPI_WIDTH = 600



class GUI(MQTT_Client):
    def __init__(self, *args, **kwargs):
        ##MQTT STUFF
        # Setup the MQTT stuff from parent
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Define my_topic
        #self.my_topic = [("TEMP", QOS_1)]
        self.my_topic = [TOPICS['temp']]
        # Subscribe to the topic. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topic))
        self.id = 2
        
        ## TKINTER STUFF
        self.root = tk.Tk()
        self.tk_interval = 0.05
        # Make the root container

        main_window = tk.Frame(self.root, height=RPI_HEIGHT, width=RPI_WIDTH)
        main_window.pack(side="top", fill="both", expand = True)
        
        # make the menu frame
        menu = tk.Frame(master=main_window, bg='lightblue')
        page = tk.Frame(master=main_window)
        self.button_dashboard = tk.Button(menu, text="Dashboard",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(Dashboard),
        )
        self.button_dashboard.pack(side=tk.LEFT)

        self.button_control = tk.Button(menu, text="Control Policy",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(UpdateControlPolicy)
        )
        self.button_control.pack(side=tk.LEFT)
        self.button_statistics = tk.Button(menu, text="Statistics",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(Statistics)
        )
        self.button_statistics.pack(side=tk.LEFT)

        self.button_about = tk.Button(menu, text="About",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(About)
        )
        self.button_about.pack(side=tk.LEFT)

        self.button_about = tk.Button(menu, text="Quit",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: exit(0)
        )
        self.button_about.pack(side=tk.LEFT)

        

        menu.pack(side=tk.TOP)
        page.pack(side=tk.TOP)

        self.frames = {}

        for F in (Dashboard, UpdateControlPolicy, Statistics, About):

            frame = F(page, self)

            self.frames[F] = frame

            frame.grid(row=0,column=0, sticky="nsew")

        self.menu_button_map = {'Dashboard': self.button_dashboard, 'UpdateControlPolicy': self.button_control, 'Statistics':self.button_statistics, 'About':self.button_about}
        self.current_button = self.button_dashboard
        self.show_frame(Dashboard)

        
        

    def show_frame(self, cont):
        self.current_button.config(relief=tk.RAISED)
        self.current_button = self.menu_button_map[cont.name]
        self.current_button.config(relief=tk.SUNKEN)
        frame = self.frames[cont]
        frame.refresh()
        frame.tkraise()
        
    def packet_received_cb(self,topic, payload_dict):
        """
        THis function will be called each time a packet is received
        This should update a display box in 
        """
        if DEBUG:
            print("DEBUG: packet_received_cb called in dummy_gui")
            print("DEBUG: topic = {} data = {}".format(topic, payload_dict['Data']))
        
        # There will be several topics. So we should do a if-elif 
        # structure to handle the different incoming packets.
        # We wish to display on the screen
        # First split the packet into its format (btw these things will eventually be implemented in functions)
        data = payload_dict['Data']
        self.frames[0].update_temperature(data)

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
        
 
class GuiFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,
                        height=RPI_HEIGHT,
                        width=RPI_WIDTH,
                        bg='white',
                        relief=tk.RIDGE)
        self.controller = controller
    
    def refresh(self):
        print("This has to be implemented. refresh page each time some shit happens")
        


class Dashboard(GuiFrame):

    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        self.temp_c = tk.DoubleVar()
        self.temp_c.set(24.3)
        label_temp = tk.Label(self, text="Temperature: ", font=LARGE_FONT)
        label_celsius = tk.Label(self, textvariable=self.temp_c, font=LARGE_FONT)
        label_control = tk.Label(self, text="Control Policy", font=LARGE_FONT)
        
        label_temp.pack(side=tk.TOP)
        label_celsius.pack(side=tk.TOP)

        f = Figure(figsize=(10,3), dpi =100)
        a_week = f.add_subplot(111)
        a_week.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP)
    
    def update_temperature(temp):
        print("YE")
        self.temp_c.set(temp)
    name = "Dashboard"


class UpdateControlPolicy(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        label = tk.Label(self, text="Update Control Policy!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


        f = Figure(figsize=(10,3), dpi =100)
        a_week = f.add_subplot(111)
        a_week.plot(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], [1,2,3,4,5,6,7])


        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP)
    
    name = "UpdateControlPolicy"

class Statistics(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        label = tk.Label(self, text="Statistics!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        f = Figure(figsize=(10,7), dpi =100)
        a_week = f.add_subplot(211)
        a_week.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        a_day = f.add_subplot(212)
        a_day.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    name = "Dashboard"
class About(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        
        label = tk.Label(self, text="About!!!", font=LARGE_FONT)
        label.pack()
    name = "About"

        


if __name__ == '__main__':
    GUI = GUI()
    GUI.run()
