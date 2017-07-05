# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import sys

MQTT_ADDRESS = 'iot.eclipse.org'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60

if sys.version_info[0] == 3:
    input_func = input
else:
    input_func = raw_input


def on_connect(client, userdata, flags, rc):
	#Aqui deve ocorrer a "inscrição" no topico desejado    

def on_subscribe(client, userdata, mid, granted_qos):
    print('Inscrito no tópico: %d' % mid)


def on_message(client, userdata, msg):
	#A mensagem enviada pelo publisher é tratada aqui    


def loop():
	#Defina aqui a conexão, o que ocorre durante um on_connect, on_subscribe e on_message
	# Lembre-se que deve estar em looping. O paho.mqtt possui uma função que faz isso    
	client = mqtt.Client()
	client.on_connect = on_connect

if __name__ == '__main__':
    #chamada para a função loop
