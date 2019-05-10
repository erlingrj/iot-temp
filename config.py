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