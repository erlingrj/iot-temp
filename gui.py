# Dummy GUI just printing date + current temp to the stdout
from mqtt_client import MQTT_Client
from hbmqtt.mqtt.constants import QOS_1
import asyncio
import copy

# Configuration of TOPICS and addresses
from config import *
# GUI configuration and texts
from gui_config import *

# For exception handeling
import sys
import os

# For accessing the log files:
import logger


# Just a variable used for conditional debugging prints
DEBUG = True


import tkinter as tk
from tkinter import ttk
import math

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent
import matplotlib.pyplot as plt


class GUI(MQTT_Client):
    def __init__(self, *args, **kwargs):
        ##MQTT STUFF
        # Setup the MQTT stuff from parent
        # Initialize the MQTT_client parent class
        MQTT_Client.__init__(self)
        # Define my_topic
        #self.my_topic = [("TEMP", QOS_1)]
        self.my_topic = [TOPICS['temp'], TOPICS['temp_setpoint']]
        # Subscribe to the topic. This is done by letter asyncio-loop run that co-routine until completion
        # I.e. we will do that before continuting to the rest of the program.
        self.loop.run_until_complete(self.subscribe_to(self.my_topic))
        self.id = 2

        self.current_temp = 18.0
        self.current_control = copy.deepcopy(logger.get_current_control_policy())

        ## TKINTER STUFF
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.tk_interval = 0.05
        # Make the root container which contains menu and page
        main_window = tk.Frame(self.root, height=RPI_HEIGHT, width=RPI_WIDTH)
        main_window.pack(side="top")
        
        # make the menu frame
        menu = tk.Frame(master=main_window, bg='lightblue', width=RPI_WIDTH)
        page = tk.Frame(master=main_window, width=RPI_WIDTH)

        # Make buttons in menu
        self.button_dashboard = tk.Button(menu, text="Dashboard",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(Dashboard),
                                   relief=tk.SUNKEN
        )
        self.button_dashboard.pack(side=tk.LEFT)

        self.button_control = tk.Button(menu, text="Control Policy",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(UpdateControlPolicy),
                                   relief=tk.RAISED
        )
        self.button_control.pack(side=tk.LEFT)
        self.button_statistics = tk.Button(menu, text="Statistics",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(Statistics),
                                   relief=tk.RAISED
        )
        self.button_statistics.pack(side=tk.LEFT)

        self.button_about = tk.Button(menu, text="About",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.show_frame(About),
                                   relief=tk.RAISED
        )
        self.button_about.pack(side=tk.LEFT)

        self.button_quit = tk.Button(menu, text="Quit",
                                    bg=MENU_BUTTON_COLOR,
                                    font=MENU_BUTTON_FONT,
                                    width=MENU_BUTTON_WIDTH,
                                    height=MENU_BUTTON_HEIGHT,
                                   command= lambda: self.shut_down(),
                                   relief=tk.RAISED
        )
        self.button_quit.pack(side=tk.LEFT)

        # Pack menu and page
        menu.pack(side=tk.TOP)
        page.pack(side=tk.TOP)

        # Make all the frames and stack them ontop of each other
        self.frames = {}

        for F in (Dashboard, UpdateControlPolicy, Statistics, About):
            frame = F(page, self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")
        
        # Current page=button is pressed
        self.menu_button_map = {'Dashboard': self.button_dashboard, 'UpdateControlPolicy': self.button_control, 'Statistics':self.button_statistics, 'About':self.button_about}
        self.current_button = self.button_dashboard
        self.show_frame(Dashboard)

        # This function is called whenever we wanna change frame.
        # It brings the desired frame to the top of the stack
    def show_frame(self, cont):
        self.current_button.config(relief=tk.RAISED)
        self.current_button = self.menu_button_map[cont.name]
        self.current_button.config(relief=tk.SUNKEN)
        frame = self.frames[cont]
        frame.refresh()
        frame.tkraise()
        print(self.current_button)
        
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
        if topic == TOPICS['temp'][0]: 
            if DEBUG:
                print("GUI recv new temp")  
            data = payload_dict['Data']
            self.current_temp = data
            self.frames[Dashboard].update_temperature(data)
        elif topic == TOPICS['temp_setpoint'][0]:
            if DEBUG:
                print("GUI recv new control_policy")
            data = [float(x) for x in payload_dict['Data'].split('-')]
            self.current_control = [CONTROL_LABELS,data]
            self.frames[Dashboard].update_control(self.current_control)
        elif topic == TOPICS['controller']:
            if DEBUG:
                print("GUI recv new controller ONOFF")
            

    
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
        except:
            pass
            



    async def run_tk(self):
        """
        Run TK with asyncio
        """
        while True:
            self.root.update()
            self.root.update_idletasks()
            await asyncio.sleep(self.tk_interval) #tk_interval is defined in the __init__

    def shut_down(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()

        self.root.destroy()
        self.loop.stop()
        os._exit(0)

        
 
 # GUI frame is the parent of all the frames
 # Any general code is implemented here
class GuiFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,
                        height=RPI_HEIGHT,
                        width=RPI_WIDTH,
                        bg='white')
        self.controller = controller
        self.parent = parent
    
    def refresh(self):
        pass    
    

# Dashboard frame
class Dashboard(GuiFrame):

    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        self.temp_c = tk.DoubleVar()
        self.temp_c.set(24.3)
        label_temp = tk.Label(self, text="Temperature: ", font=LARGE_FONT)
        label_celsius = tk.Label(self, textvariable=self.temp_c, font=XL_FONT)
        
        label_temp.pack(side=tk.TOP)
        label_celsius.pack(side=tk.TOP)

        self.figure = Figure(figsize=(FIGSIZE_X, FIGSIZE_Y-0.5))
        self.control_plot = self.figure.add_subplot(111, ylabel="Temp [C]", title="Control Policy")
        self.control_plot.set_ylim([MIN_CONTROL_TEMP, MAX_CONTROL_TEMP])
        self.control_plot.plot(controller.current_control[0], controller.current_control[1], "ro-")
        self.control_plot.grid()
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP)
        self.figure.autofmt_xdate(rotation=45)

    def plot(self, figure, data):
        figure.clf()
        self.control_plot = self.figure.add_subplot(111, ylabel="Temp [C]", title="Control Policy")
        self.control_plot.plot(data[0], data[1], "ro-")
        self.control_plot.set_ylim([MIN_CONTROL_TEMP, MAX_CONTROL_TEMP])
        self.figure.autofmt_xdate(rotation=45)
        self.control_plot.grid()
        figure.canvas.draw_idle()

    
    def update_temperature(self, temp):
        self.temp_c.set(("{:.2f}C".format(float(temp))))

    def update_control(self, control):
        self.plot(self.figure, control)

    def refresh(self):
        self.plot(self.figure, self.controller.current_control)

    

    name = "Dashboard"


# Update control policy frame
class UpdateControlPolicy(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)

        button_update = tk.Button(self, text="Save", command= lambda: self.update_control())
        button_reset = tk.Button(self, text="Reset", command = lambda : self.reset_control())

        
        
        self.control_editable = copy.deepcopy(controller.current_control)

        self.figure = Figure(figsize=(FIGSIZE_X_CTRL, FIGSIZE_Y_CTRL))
        
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP)

        self.figure.canvas.mpl_connect('button_press_event', self._on_click)
        self.figure.canvas.mpl_connect('button_release_event', self._on_release)
        self.figure.canvas.mpl_connect('motion_notify_event', self._on_motion)
        self._dragging_point = None

        button_update.pack(side=tk.LEFT)
        button_reset.pack(side=tk.LEFT)

        

    
    name = "UpdateControlPolicy"

    def plot(self,figure,data):
        self.figure.clf()
        self.figure.canvas.draw_idle()
        self.control_plot = self.figure.add_subplot(111,xlabel='Time',ylabel='Temp[C]')
        self.control_plot.tick_params(axis='x', which='major', labelsize=SUBPLOT_XTICKS_SIZE)
        self.control_plot.set_ylim([MIN_CONTROL_TEMP, MAX_CONTROL_TEMP])
        self.control_plot.set_title("Change Control Policy", fontsize=PLOT_TITLE_SIZE)
        self.control_plot.plot(data[0], data[1], "ro-")
        self.control_plot.grid()
        self.figure.autofmt_xdate(rotation=45)


    def refresh(self):
        self.control_editable = copy.deepcopy(self.controller.current_control)
        self.plot(self.figure, self.control_editable)

    def update_control(self):
        self.controller.current_control = copy.deepcopy(self.control_editable)
        payload = "-".join(map(str,self.control_editable[1]))
        # The we call the async function publish_to with the right topic
        # We use ensure_future as it is an async function and we cannot call await on it
        # since we are inside a non-async function
        asyncio.ensure_future(self.controller.publish_to(TOPICS['temp_setpoint'][0], payload) )

    def reset_control(self):
        self.refresh()

    def _on_click(self, event):
        
        if event.button == 1 and event.inaxes in [self.control_plot]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
    
    def _on_release(self, event):
        if self._dragging_point:
            self._dragging_point = None

    def _on_motion(self, event):
        if self._dragging_point:
            self.control_editable[1][self._dragging_point] = event.ydata
            self.plot(self.figure, self.control_editable)
    
    def _find_neighbor_point(self, event):
        distance_threshold = 1
        nearest_point = None
        min_distance = 10000
        for x, y in enumerate(self.control_editable[1]):
            zz=event.xdata
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = x
        if min_distance < distance_threshold:
            return nearest_point
        return None


    
class Statistics(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        self.figure = Figure(figsize=(FIGSIZE_X, FIGSIZE_Y))
        
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP)


    def plot(self, figure, last_week, last_24h):
        figure.clf()
        self.week_plot = figure.add_subplot(211)
        self.week_plot.set_title("Last week", fontsize=SUBPLOT_TITLE_SIZE)
        self.week_plot.tick_params(axis='x', which='major', labelsize=SUBPLOT_XTICKS_SIZE)
        self.week_plot.set_ylim([MIN_TEMP, MAX_TEMP])
        self.week_plot.set_xlim([0,23])
        self.week_plot.plot(last_week[0], last_week[1], "bo-")
        self.week_plot.grid()

        self.day_plot = figure.add_subplot(212)
        self.day_plot.set_title("Last 24 hours", fontsize=SUBPLOT_TITLE_SIZE)
        self.day_plot.tick_params(axis='x', which='major', labelsize=SUBPLOT_XTICKS_SIZE)
        self.day_plot.set_ylim([MIN_TEMP, MAX_TEMP])
        self.day_plot.set_xlim([0,23])
        self.day_plot.plot(last_24h[0], last_24h[1], "bo-") 
        self.day_plot.grid()

        plt.setp(self.week_plot.get_xticklabels(), rotation=45, ha='right')
        plt.setp(self.day_plot.get_xticklabels(), rotation=45, ha='right')

        figure.tight_layout()
        figure.canvas.draw_idle()


    def refresh(self):
        last_24h = logger.get_temp_24h()
        last_week = logger.get_temp_1w()
        self.plot(self.figure,last_week,last_24h)

    name = "Dashboard"
class About(GuiFrame):
    def __init__(self, parent, controller):
        GuiFrame.__init__(self,parent,controller)
        text = tk.Text(self, height=ABOUT_TEXT_HEIGHT, width=ABOUT_TEXT_WIDTH)
        text.insert(tk.END, ABOUT_TEXT)
        text.pack(side=tk.TOP)
    name = "About"

        

def run():
    G = GUI()
    G.run()



if __name__ == '__main__':
    run()
