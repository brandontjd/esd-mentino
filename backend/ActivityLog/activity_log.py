#!/usr/bin/env python3

import sys
import json
from os import environ
from channel import Channel

import logging
from logdna import LogDNAHandler

hostname = environ.get("RABBITMQ_HOSTNAME", default="localhost")
port = int(environ.get("RABBITMQ_PORT", default="5672"))
exchangename = "esd_exchange"
exchangetype = "topic"

pika_channel = Channel(
    hostname,
    port,
    exchangename,
    exchangetype
)

monitorBindingKey='*.log'

log = logging.getLogger('logdna')
log.setLevel(logging.INFO)
log.addHandler(LogDNAHandler(environ.get("LOGDNA_INGESTION"), { "hostname": "mentino" }))

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log")
    try:
        payload = json.loads(body)
        error_type = payload["type"]

        logdna_params = [body.decode("utf-8"), { "app": "activity_log" }]
        if error_type == "info":
            log.info(*logdna_params)
        elif error_type == "warning":
            log.warning(*logdna_params)
        elif error_type == "error":
            log.error(*logdna_params)
    except Exception as e:
        log.error("Error in activity log: " + body)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, exchangename))

    pika_channel.set_consume_callback(queue="activity_log", callback=callback)
    pika_channel.start_consuming()