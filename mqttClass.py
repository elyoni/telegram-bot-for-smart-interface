#For mqtt
import paho.mqtt.client as mqtt

class mqttClass:
    def on_connection(self, client, obj, flags, rc):
        print ("You are connected to the MQTT Server")
        self.subscribeEnabler(client)

    def on_message(self,client, userdata, msg):
        newMsg=(str(msg.payload))
				# print newMsg
        self.mqttCallbacks[msg.topic](str(msg.payload))

    def __init__(self,mqttServerIp = "127.0.0.1"):
        self.mqtt_client = mqtt.Client()#(client_id="Telegram Bot")
        self.mqtt_client.on_connect = self.on_connection
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(mqttServerIp,port = 1883, keepalive = 60)
        self.mqtt_client.publish("debug","connected to the server")
        self.mqttCallbacks = {}
        
    def startLoopMQTT(self):
        self.mqttSubscribeHandler()
        self.mqtt_client.loop_start()

    def mqttSubscribeHandler(self):
        # The user will add his subscibe and the function to run
        # Example: addNewSubscribe('torrent',torrentFucn)
        None

    def subscribe(self,name,callback):
        #Dont Use the same subscribeName
        self.mqttCallbacks[name] = callback

    def subscribeEnabler(self,client):
        for mqttSubscribeName in self.mqttCallbacks.keys():
            client.subscribe(mqttSubscribeName) 
