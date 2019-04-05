This is a working progress. Will elaborate on my ideas later.

# High Level Design
2 main base classes:
 
## MQTT Server Base Class (abstract)
* init()

## MQTT Client Base Class (abstract)
Inherits from: hbmqtt-client
Public
* init()
    - Takes some parameters and sets up the connection to the broker.
* publish(address, packet)
    - Publishes a packet to the broker
* subscribe(address)
    - Subscribes to an address with the broker

Private:
* packet_received_callback() = 0 (is pure virtual)
    - Is called whenever the client receives a packet




### Sensor class (abstract)
Inherits from: MQTT Client Base Class
Public:
* init_sensor(int sampling_fq) = 0
    - Sets up the hardware and SPI interface to the sensor
    - Sets up a loop reading the sensor at specific intervals
* packet_received_callback() = 0
    - It implements this function. 

#### Temperature Sensor class



### UI Class (Abstract)
Inherits from: MQTT Client Base Class
Public:
* init()
    - Subscribe to the correct addresses
* publish_setpoint(setpoint)
    - Publish a user setpoint to the controller
* 
* request_sensor_data(sensorID)
    - requests data from a sensor
#### GUI Class

#### Voice UI Class

#### WEB GUI Class


### Controller Class (abstract)
Inherits from: MQTT Client Base Class
Public:
* init():
    - Subscribe to correct addresses
* publish_new_setpoint(setpoint)
    - Publishes a newly accepted setpoint
* set_controls(controls) = 0
* request_sensor_data()
* packet_received_callback() = 0

#### Temperature Controller Class




### Storage Class (abstract)
Inherits from: MQTT Client Base Class
Public:
* store(entry) = 0
* retrieve(time) = 0
* packet_received_callback()
