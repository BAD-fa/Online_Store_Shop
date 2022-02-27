import uuid
from discountcode_app.discount_code.setting import rabbit_connection,pika


class DiscountCodeRpcClient(object):

    def __init__(self):
        self.connection = rabbit_connection

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='discount_code_app',exchange_type='direct')


        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self,user_id_list,expire_time):
        self.response = None
        self.corr_id = uuid.uuid4()
        self.channel.basic_publish(
            exchange='discount_code_app',
            routing_key='discount_code_get',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body={"user_id_list":user_id_list,"expire_time":expire_time})
        while self.response is None:
            self.connection.process_data_events()
        return self.response
