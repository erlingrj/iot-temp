## Introduction
With the advent of cheap microcontroller with networking capabilities solutions for automation in buildings is gaining traction. Our hypothetical customer is large scale industrial, public or commercial buildings like factories, universities or hotels. The aim of the project is to create a system for measuring and controlling the temperature in a building as well as providing an intuitiv interface to the system. There is an emphasis on using the M2M protocol MQTT for communication purposes. 

## Requirements
* A single temperature sensor connect through a Raspberry Pi
* A graphical user interface implemented on a Raspberry Pi with an LCD screen
* A web user interface
* Emulate a temperature controller with the Raspberry Pi
* Raspberry should keep a local and a remote log
* 


## Technology

### Raspberry PI
The RPi is the key component in this system. It serves several functions that typically, for our hypothetical customers, would be divided between several components spread out over the building. Each of the functions are running in a separate process and communicating with another through MQTT thus we have a very scalable system.

#### Temperature Sensing
The sensor process is polling the external temperature sensor at a user-specify interval. Each sample is broadcasted on a dedicated MQTT topic.

#### Temperature Controlling
The controller process is emulating a temperature cntroller. It is implementing the simplest control algorithm. The heating system is turned ON when the temperature falls below the desired temperature and its turned OFF when it rises above the desired temperature. This control algorithm would result in a marginally stable system where the temperature would oscillate around the setpoint. To get a stable and fast system a PID controller or a Kalman filter could be implemented.

The controller process is subscribing to both the temperature topic and the control policy topic.

#### Graphical User Interface
The graphical user interface process displays the current temperature on the LCD screen and lets the user update the control policy and also 

#### Logger/Gateway

#### MQTT Broker


### Amazon Web Services

### MQTT

## Framework and languages

### Raspberry Pi

### Amazon Web Services





