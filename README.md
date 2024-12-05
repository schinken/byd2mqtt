# byd2mqtt

This lovely little repository provides a handy Python script that'll help you bridge the communication between your BYD HVS energy storage systems and other Modbus RTU and MQTT-based systems.

The script reads data from your BYD HVS Modbus RTU packages, parses it into meaningful metrics, and publishes these metrics as MQTT messages to a specified broker. This makes it super easy to integrate your BYD HVS data into home automation platforms, IoT systems, or other monitoring tools.

## Docker

```bash
docker build -t byd2mqtt .
docker run -e MQTT_HOST=my.mqtt.server.org --rm byd2mqtt
```

## Environment Variables

- **`MQTT_HOST`**: Hostname or IP of the MQTT broker (default: `test.mosquitto.org`).
- **`MQTT_PORT`**: Port of the MQTT broker (default: `1883`).
- **`MQTT_BASE_TOPIC`**: Base topic for MQTT messages (default: `infrastructure/pv/byd`).
- **`BYD_IP`**: IP address of the BYD HVS device (default: `192.168.16.254`).
- **`BYD_PORT`**: Port for the BYD HVS Modbus RTU (default: `8080`).

# Thanks

Thanks to:

* https://github.com/christianh17/ioBroker.bydhvs
* https://github.com/robertdiers/solar-manager/blob/main/python/BYD.py