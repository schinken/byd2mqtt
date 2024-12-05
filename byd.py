#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os
import socket

BUFFER_SIZE = 1024
MESSAGE_1 = "010300000066c5e0" #read serial
MESSAGE_2 = "01030500001984cc" #read data

mqtt_host = os.getenv("MQTT_HOST") or "test.mosquitto.org"
mqtt_port = os.getenv("MQTT_PORT") or 1883
mqtt_base_topic = os.getenv("MQTT_BASE_TOPIC") or "infrastructure/pv/byd"

byd_ip = os.getenv("BYD_IP") or "192.168.16.254"
byd_port = os.getenv("BYD_PORT") or 8080

def buf2int16SI(byteArray, pos): #signed
    result = byteArray[pos] * 256 + byteArray[pos + 1]
    if (result > 32768):
        result -= 65536
    return result

def buf2int16US(byteArray, pos): #unsigned
    result = byteArray[pos] * 256 + byteArray[pos + 1]
    return result

def read_byd(ip, port):  
    try: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(bytes.fromhex(MESSAGE_2))
        data = client.recv(BUFFER_SIZE)
    finally:
        client.close()

    outvolt = buf2int16US(data, 35) * 1.0 / 100.0
    maxvolt = buf2int16SI(data, 5) * 1.0 / 100.0
    minvolt = buf2int16SI(data, 7) * 1.0 / 100.0
    ampere = buf2int16SI(data, 11) * 1.0 / 10.0

    return {
        "soc": buf2int16SI(data, 3),
        "maxvolt": maxvolt,
        "minvolt": minvolt,
        "soh": buf2int16SI(data, 9),
        "ampere": ampere,
        "battvolt": buf2int16US(data, 13) * 1.0 / 100.0,
        "maxtemp": buf2int16SI(data, 15),
        "mintemp": buf2int16SI(data, 17),
        "battemp": buf2int16SI(data, 19),
        "error": buf2int16SI(data, 29),
       # "paramt": chr(data[31]) + "." + chr(data[32]),
        "outvolt": outvolt,
        "power": round((ampere * outvolt) * 100 / 100, 2),
        "diffvolt": round((maxvolt - minvolt) * 100 / 100, 2),
    }
    

try:
    result = read_byd(byd_ip, byd_port)
    print(result)

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(mqtt_host, mqtt_port, 60)

    for key, value in result.items():
        mqttc.publish(f"{mqtt_base_topic}/{key}", value)

except Exception as ex:
    print ("ERROR BYD: ", ex)