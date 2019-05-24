from hbmqtt.mqtt.constants import QOS_1

TOPICS = {'temp': ('temp', QOS_1), 'temp_setpoint' : ('setpoint_topic', QOS_1), 'ping' : ('ping_topic', QOS_1)}
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

DB_GET_TEMP_PATH = "http://127.0.0.1:5000/db/get-last-temp"
DB_GET_CONTROL_PATH = "http://127.0.0.1:5000/db/get-last-control"
DB_POST_TEMP_PATH =  "http://127.0.0.1:5000/db/post-temp"
DB_POST_CONTROL_PATH = "http://127.0.0.1:5000/db/post-control"


APIKEY= 12345
{	
	"APIKEY" : 12345,
	"TimeStamp" : "17-05-2019-12-14-12",
	"Data"	: "22.5"
}