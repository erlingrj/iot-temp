import os
import time
import multiprocessing
from multiprocessing import Process

from ping_service import pingService
import gui
import mqtt_server
import controller
import sensor
import logger

if __name__ == '__main__':
    multiprocessing.set_start_method('forkserver', force='true')
    procs = []
    P_broker = Process(target=mqtt_server.run_broker)
    procs.append(P_broker)
    P_gui = Process(target=gui.run)
    procs.append(P_gui)
    P_controller = Process(target=controller.run)
    procs.append(P_controller)
    P_sensor = Process(target=sensor.run)
    procs.append(P_sensor)
    P_logger = Process(target=logger.run)
    procs.append(P_logger)
    P_ping = Process(target=pingService.run)
    procs.append(P_ping)

    for p in procs:
        p.start()
        time.sleep(1)

    for p in procs:
        p.join()

    # os.system("python3 mqtt_server.py")
    # os.system("python3 logger.py")
    # os.system("python3 dummy_temp_sensor.py")
    # os.system("python3 dummy_temp_controller.py")
    # os.system("python3 gui.py")

