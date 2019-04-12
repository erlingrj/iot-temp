# iot-temp
IOT project using RPi and MQTT

MQTT_Client.py implements an abstract base class that we will use to derive all our objects from.

dummy-temp-sensor.py inherits from MQTT_Client and is modelling the behaviour of a real temperature sensor. He will publish a random temperature to the "TEMP" topic every second.

dummy-gui.py also inherits from MQTT_Client. He subscribes to TEMP and will display the latest temp on the stdout (terminal). The classes and methods should be further refined but they serve as a starting point for developing the REAL GUI and the REAL temp sensor. 

Code example of asyncio+tkinter:
https://gist.github.com/nameoftherose/037e97b95d94df7867ee328ea8009857

Quick intro to asyncio1:
https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/

Intro to asyncio2:
https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/


