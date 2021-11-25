# Send UDP broadcast packets

MYPORT = 2020

import sys, time
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    data = repr(time.time()) + '\n'
    s.sendto(bytes(data, encoding = 'utf-8'), ('<broadcast>', MYPORT))
    time.sleep(2)
