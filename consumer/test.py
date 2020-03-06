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
print(next(consumer))