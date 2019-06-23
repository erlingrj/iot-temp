from hbmqtt.mqtt.constants import QOS_1

TOPICS = {'temp': ('/sensors/temperature', QOS_1), 'temp_setpoint' : ('/user/control_policy', QOS_1), 'ping' : ('ping_topic', QOS_1)}
REMOTE_AWS_GROUP_ID = 49
BROKER_ADDR = 'ws://localhost:8080/'
# THis is the default config of the Broker
BROKER_CONFIG = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883',
            'max_connections': 10
        },
        'ws': {
            'type': 'ws',
            'bind': 'localhost:8080', # THis must match the connectin Clients
            'max_connections': 10
        },
    },
    'sys_interval': 0,
    'auth': {
        'allow-anonymous': True
    },
    'plugins' : ['auth_anonymous'],
    'topic-check' : {
        'enabled' : True,
        'plugins' : ['topic_taboo'], #This is important for allowing subscribing to random topics
    },
}



WEBSERVICE_IP = 'localhost'
WEBSERVICE_PORT = 8888

LOG_FILE_PATH = 'log/log.txt'
CURRENT_POLICY_PATH = 'log/current-control.txt'

SERVER_PATH = "http://127.0.0.1:5000"
# "http://35.180.58.140"

DB_GET_TEMP_PATH = "{}/db/get-last-temp".format(SERVER_PATH)
DB_GET_CONTROL_PATH = "{}/db/get-last-control".format(SERVER_PATH)
DB_POST_TEMP_PATH =  "{}/db/post-temp".format(SERVER_PATH)
DB_POST_CONTROL_PATH = "{}/db/post-control".format(SERVER_PATH)

TEMP_SAMPLING_INTERVAL = 15*60

APIKEY="8c5118e342801a9aa6128978f93e321d762e3aea"



DEVICE_MAC = "02:01:04:02:01:01"