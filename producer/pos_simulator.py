from kafka import KafkaProducer
from datetime import datetime
import uuid
import requests
import json
from settings import *
import random
import time

headers = dict()
headers['auth_key'] = 'e1dfc3aa6ad378a2d2aa7564cfcc42b1ad49c28840f2fc7dd9d275ab857b9f03'
# cities = json.loads(requests.get('https://www.bigbasket.com/auth/get_footer/?city_id=1').text).get('cities')
cities = ['Kadapa', 'Hyderabad', 'Bangalore', 'Chennai']
fruits_url = 'https://grofers.com/v4/search/merchants/26659/products/?l0_cat=1487&start=0&next=100'
producer = KafkaProducer(bootstrap_servers=servers,
                         value_serializer=lambda m: json.dumps(m).encode('ascii'),
                         api_version=(1,10,0))
inventory = dict()


def get_fruits():
    json_data = json.loads(requests.get(fruits_url, headers=headers).text)
    json_data = json_data.get('result').get('products')
    for fruit in json_data:
        fruit_item = dict()
        fruit_item['price'] = fruit.get('price')
        fruit_item['discount'] = fruit.get('discount')
        inventory[fruit.get('name')] = fruit_item


def generate_orders():
    while True:
        order_data = dict()
        order_data['invoice_id'] = uuid.uuid4().time
        order_data['invoice_data'] = str(datetime.now().date())
        items = list()
        for i in range(random.choice(range(1, 25))):
            item_data = dict()
            item_data['name'] = random.choice(list(inventory.keys()))
            item_data['unit_price'] = inventory.get(item_data['name']).get('price')
            item_data['total_units'] = random.choice(range(1,10))
            item_data['amount'] = item_data['total_units'] * item_data['unit_price']
            items.append(item_data)
        order_data['items'] = items
        order_data['order_total'] = sum([item.get('amount') for item in items])
        order_data['city'] = random.choice(cities)
        order_data['payment_mode'] = random.choice(['Cards & Digital', 'Cash'])
        order_data['is_member'] = random.choice([True, False])
        future = producer.send('orders', value=json.dumps(order_data))
        print(future.get())
        print(order_data)
        # time.sleep(1)

get_fruits()
generate_orders()