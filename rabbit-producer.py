import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=32785))
channel = connection.channel()

for i in range(1, 15):
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    time.sleep(2)
connection.close()
