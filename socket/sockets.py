#!/usr/bin/python           # This is client.py file
import sockets               # Import socket module
import random

g=101 # publicly known
p=103 # publicly known

y= random.randint(1,100) # Bob's random number



for i in range(1, 10000):
    s = sockets.sockets()  # Create a socket object
    host = sockets.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.

    s.connect((host, port))