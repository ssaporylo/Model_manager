#!/usr/bin/env python
import pika
import redis
import datetime


def start(r):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='models')

    def callback(ch, method, properties, body):
        key = str(datetime.datetime.now())
        r.set(key, body)
        data = '{0}: {1}'.format(key, body)
        r.publish('first_channel', data)
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue='models',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start(redis.StrictRedis(host='localhost', port=6379, db=0))
