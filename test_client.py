from math import trunc
from random import random
import datetime

from libnine.nine_client import nine_client
from libnine.nine_types import msg_type
from libnine import nine_pb2

# Construct a client
#  You can change the port, network and network interface name through parameters
#  Usage: nine_client(20001, '192.168.100.255', 'usb0')
connection = nine_client(20001)
connection.discover_server()

# Construct a random Onesecond message
msg = nine_pb2.Onesecond()
msg.ts.FromDatetime(datetime.datetime.now())

for x in range(60):
    pos = msg.positions.add()
    pos.x = trunc(random() * 100)
    pos.y = trunc(random() * 100)
    pos.z = trunc(random() * 100)

# Send message
connection.send(msg_type.onesecond, msg)
