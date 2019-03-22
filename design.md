This is a working progress. Will elaborate on my ideas later.

### High Level Design
2 main base classes:
 
#### MQTT Server Class
* init()

#### MQTT Client Class

Functions:
* init()
* publish(address, packet)
* subscribe(address)
* packet_received_callback(address, packet)

Sub Classes:
1. Sensor
Functions:
* init()

2. Controller
Functions:
* init()
* ctrl_loop()
* set_setpoint(setpoint)

3. UI
Functions:
* init()
* ctrl_loop()
* display_data(data)
* user_input_callback(data)


    - LCD Screen UI
    - Web Browser UI
    - Voice control UI
4. Storage
    - Local database
    - Cloud database


