import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import animation
import numpy
import random
from settings import *
import json
from kafka import KafkaConsumer
from matplotlib.animation import FuncAnimation

consumer = KafkaConsumer(bootstrap_servers=servers,
                         value_deserializer=lambda m: json.loads(m).encode('ascii'),
                         api_version=(1,10,0))

consumer.subscribe(['orders'])

cities = ['Kadapa', 'Hyderabad', 'Bangalore', 'Chennai']
city_amount = {city_name:0 for city_name in cities}

y_pos = np.arange(len(cities))

ax = plt.bar(y_pos, list(city_amount.values()), align='center', alpha=0.5)

plt.xticks(y_pos, cities)
plt.ylabel('Total Amount')
plt.title('Order Total Amountwise!')


def animate(i):
    print('Frame number is {}'.format(str(i)))
    data = next(consumer).value
    city_name = json.loads(data).get('city')
    city_amount[city_name] = city_amount.get(city_name, 0) + json.loads(data).get('order_total')
    performance = list(city_amount.values())
    for i, data in enumerate(performance):
        plt.yticks(performance)
        ax.patches[i].set_height(data)
        import time
    # plt.bar(y_pos, performance, align='center', alpha=0.5)

anim = animation.FuncAnimation(plt.gcf(), animate,
                               frames=200, interval=100, blit=False)

plt.show()