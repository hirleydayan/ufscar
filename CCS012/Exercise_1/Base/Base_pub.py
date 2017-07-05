# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import sys
import time

#Biblioteca que pode ser utilizada para fazer a varedura sobre arquivos em um diretório
from os import walk

# Servidor eclipse que roda o mosquitto(um broker)
MQTT_ADDRESS = 'iot.eclipse.org' 
#Porta de escuta
MQTT_PORT = 1883

MQTT_TIMEOUT = 60

if sys.version_info[0] == 3:
    input_func = input
else:
    input_func = raw_input


def send_message(msg):
	#Defina aqui a conexão e publicação das mensagens.	

if __name__ == '__main__':
	# Chama para o send_message
	# Você pode modelar a mensagem aqui
