'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import datetime 
AllowedActions = ['both', 'publish', 'subscribe']

class PingService():
    def __init__(self):

        # Read in command-line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--endpoint", action="store", default="a3cezb6rg1vyed-ats.iot.us-west-2.amazonaws.com", dest="host", help="Your AWS IoT custom endpoint")
        parser.add_argument("-r", "--rootCA", action="store", default="root-CA.crt", dest="rootCAPath", help="Root CA file path")
        parser.add_argument("-c", "--cert", action="store", default="PL-student.cert.pem", dest="certificatePath", help="Certificate file path")
        parser.add_argument("-k", "--key", action="store", default="PL-student.private.key", dest="privateKeyPath", help="Private key file path")
        parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
        parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                            help="Use MQTT over WebSocket")
        parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="pl19-99",
                            help="Targeted client id")
        parser.add_argument("-t", "--topic", action="store", dest="topic", default="pl19/event", help="Event topic")
        parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                            help="Operation modes: %s"%str(AllowedActions))
        parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                            help="Message to publish")
        
        args = parser.parse_args()
        self.host = args.host
        self.rootCAPath = args.rootCAPath
        self.certificatePath = args.certificatePath
        self.privateKeyPath = args.privateKeyPath
        self.port = args.port
        self.useWebsocket = args.useWebsocket
        self.clientId = args.clientId
        self.topic = args.topic
        
        if args.mode not in AllowedActions:
            parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
            exit(2)
        
        if args.useWebsocket and args.certificatePath and args.privateKeyPath:
            parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
            exit(2)
        
        if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
            parser.error("Missing credentials for authentication.")
            exit(2)
        
        # Port defaults
        if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
            self.port = 443
        if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
            self.port = 8883
        
        # Configure logging
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        
        # Init AWSIoTMQTTClient
        self.mqtt_client = None
        self.mqtt_client = AWSIoTMQTTClient(self.clientId)
        self.mqtt_client.configureEndpoint(self.host, self.port)
        self.mqtt_client.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)
        
        # AWSIoTMQTTClient connection configuration
        self.mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec
        

    def start(self):
        self.mqtt_client.connect()
        self.mqtt_client.subscribe("pl19/notification", 1, self.customCallback)
        time.sleep(2)
        
        while True:
            time.sleep(5)
    def replyToPing(self,sequence):
        pingData = {}
    
        pingData['sequence'] = sequence
        pingData['message'] = "Ping response."
    
        message = {}
        message['device_mac'] = "b8:27:eb:f1:96:c4"
        message['timestamp'] = str(datetime.datetime.now())
        message['event_id'] = 1
        message['event'] = pingData
        messageJson = json.dumps(message)
        self.mqtt_client.publishAsync("pl19/event", messageJson, 1)
    
        print('Published topic %s: %s\n' % (self.topic, messageJson))
    
    # Custom MQTT message callback
    def customCallback(self,client, userdata, message):
        print("Received a new message: ")
        messageContent = json.loads(message.payload.decode('utf-8'))
        messageData = messageContent['event']
        print(messageContent)
        print(messageData['message'])
        print("Sequence ", messageData['sequence'])
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        if messageContent['event_id'] == 0:
            self.replyToPing(messageData['sequence']);

def run():
    PS = PingService()
    PS.start()

if __name__ == '__main__':
    run()

