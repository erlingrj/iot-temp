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

https://gist.github.com/nameoftherose/037e97b95d94df7867ee328ea8009857

https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/

