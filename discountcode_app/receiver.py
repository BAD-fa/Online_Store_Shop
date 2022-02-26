import requests
import json
import pika

from discount_code.setting import rabbit_connection


channel = rabbit_connection.channel()

channel.queue_declare(queue='discount_code_get')
channel.exchange_declare(exchange='discount_code_app',exchange_type='direct')
channel.queue_bind(exchange='discount_code_app', routing_key='discount_code_get', queue='discount_code_get')

def on_request(ch, method, props, body):

    response = requests.post("/", data = json.dumps(body), headers = {})


    ch.basic_publish(exchange='discount_code_app',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='discount_code_get', on_message_callback=on_request)

channel.start_consuming()
