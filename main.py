from helpers import send_new_variables
from datetime import datetime
from config import get_config
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        get_config('rabbitmq.host'),
        port=get_config('rabbitmq.port'),
        credentials= pika.PlainCredentials(
            get_config('rabbitmq.username'),
            get_config('rabbitmq.pass')
        ),
    )
)
rabbit_mq_channel = connection.channel()


send_new_variables(
    datetime.fromisoformat('2020-07-06 00:00:00'),
    datetime.fromisoformat('2020-07-07 00:00:00'),
    rabbit_mq_channel,
)

connection.close()
