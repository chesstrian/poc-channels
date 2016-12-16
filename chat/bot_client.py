import json
import uuid

import pika


class BotClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('quser', 'qpazzW0rd')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, command, symbol):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='bot',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(dict(command=command, symbol=symbol))
        )

        while self.response is None:
            self.connection.process_data_events()

        response = json.loads(self.response)
        return response[u'error'], response[u'text']
