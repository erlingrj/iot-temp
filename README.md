# iot-temp
IOT project using RPi and MQTT

run:
python3 mqtt-server.py
python3 mqtt-client-subscriber.py
python3 mqtt-client-publisher.py

IN THAT ORDER and also in separate terminals. Then you should see three
packets exchanged between publisher and subscriber.

The scripts are really the bare mininmal for setting up a MQTT connection
with HBMQTT. But it works.

TBC
