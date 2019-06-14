import os
from subprocess import Popen

devnull = open(os.devnull, 'wb') # Use this in Python < 3.3
# Python >= 3.3 has subprocess.DEVNULL

Popen(['nohup', 'mqtt_server.py'], stdout=devnull, stderr=devnull)
Popen(['nohup', 'logger.py'], stdout=devnull, stderr=devnull)
Popen(['nohup', 'dummy_temp_sensor.py'], stdout=devnull, stderr=devnull)
Popen(['nohup', 'dummy_temp_controller.py'], stdout=devnull, stderr=devnull)
