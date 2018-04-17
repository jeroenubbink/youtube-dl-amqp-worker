import json
import os
import shutil
import socket

from kombu import Connection, Exchange, Queue, Consumer
from youtube_dl import YoutubeDL

from config import Config

config = Config().config

rabbit_url = 'amqp://{}:{}'.format(config['AMQP_HOST'], config['AMQP_PORT'])

conn = Connection(rabbit_url)

exchange = Exchange(config['AMQP_EXCHANGE'], type=config['AMQP_EXCHANGE_TYPE'])

queue = Queue(name=config['AMQP_QUEUE_NAME'], exchange=exchange, routing_key=config['AMQP_ROUTING_KEY'])

def process_message(body, message):
    data = None
    try:
        data = json.loads(body)
    except json.JSONDecodeError as err:
        print ("Error parsing JSON payload: {0}".format(err))

    ydl = YoutubeDL()
    info = ydl.extract_info(data.get('url'))
    # FIXME: the YoutubeDL is a great commandline tool but it lacks any kind
    # of logical OO implementation hence we cannot easily manipulate any of it's
    # characteristics so we can't guess what the filename is
    # we are dealing with. Usually we should find a match on
    # '%(title)s-%(id)s.*' so we will just filter it out of the list after
    # listing the files in the directory

    # filename = DEFAULT_OUTTMPL % info

    match = '%(title)s-%(id)s.' % info
    filename = [name for name in os.listdir() if match in name]

    if len(filename) != 1:
        # produce some kind of logging event about failure,
        # maybe differentiate between different lenghts or content
        print ("shit hit the fan because we can't find the file")
        message.ack()

    filename = filename[0]
    shutil.move(filename, '{}/{}'.format(config['DOWNLOAD_LOCATION'], filename))
    message.ack()

consumer = Consumer(conn, queues=queue, callbacks=[process_message], accept=['text/plain'])
consumer.consume()

while True:
    try:
        conn.drain_events(timeout=2)
    except socket.timeout:
        pass
