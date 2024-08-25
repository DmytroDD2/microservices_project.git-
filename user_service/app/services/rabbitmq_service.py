import asyncio
import json

import pika

from .service_email import send_email


loop = asyncio.get_event_loop()


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue='user_queue')

    async def callback(ch, method, properties, body):

        await send_email(body)

    def on_message(ch, method, properties, body):
        loop.call_soon_threadsafe(lambda: asyncio.create_task(callback(ch, method, properties, body)))

    channel.basic_consume(queue='user_queue', on_message_callback=on_message, auto_ack=True)

    channel.start_consuming()


def rb_send(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='user_queue')

    channel.basic_publish(exchange='', routing_key='user_queue', body=json.dumps(message),
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

    connection.close()
