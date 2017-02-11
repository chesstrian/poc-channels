#!/usr/bin/python
import json

import pika

import commands

credentials = pika.PlainCredentials('quser', 'qpazzW0rd')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='bot')


def on_request(ch, method, props, body):
    params = json.loads(body)

    command = getattr(commands, params[u'command'])
    error, text = command(params[u'symbol'])

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(dict(error=error, text=text))
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='bot')

print(" [x] Awaiting Bot requests")
channel.start_consuming()
