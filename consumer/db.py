from pymongo import MongoClient
from settings import *
from kafka import KafkaConsumer
import json
import time
import boto3

consumer = KafkaConsumer(bootstrap_servers=servers,
                         group_id='database',
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

orders = list()
orders_limit = 1000

consumer.subscribe(['orders'])

s3 = boto3.client(endpoint_url='http://192.168.99.100:4569', service_name='s3',
                  aws_access_key_id='foo',
                  aws_secret_access_key='bar')

for msg in consumer:
    if orders_limit >= 1000:
        json.dump(orders, open('r.json', 'w'))
        file_name = 'r.json'
        s3.upload_file(
            'r.json', 'orders_data', 'orders_{}.json'.format(str(time.time()))
        )
    else:
        orders.append(json.loads(msg.value))

