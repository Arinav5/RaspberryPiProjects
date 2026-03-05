
# Week 5 Mon Network Socket
Lab Date: Feb 9 Monday
Due Date: 2:00 pm Feb 16 

## 1. HTTP Server - Static file host

* Downloaded images and placed them in the directory 
* cd into the directory 
* ran ifconfig to find the IP address of the Pi 
* ran python3 -m http.server 8000 to make the Pi act as a server on that directory 
* from personal laptop ran http://<pi_ip>:8000
* Was able to look at and download images from personal laptop 
* When clicking on the images a GET request appeared on the Pi
* Was able to access neighbor's server in a similar way by changing the IP address

## 2. socket - Low-level networking interface

Write the code for the server to run on the Pi 

```Python
import socket

HOST = ''
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
            


```

Write the code for the client to run on the personal computer

```Python 
# Echo client program
import socket

HOST = '10.144.113.15'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
```

When the server code is ran it will wait for the client connection. When the client code is ran it will send the "hello world" that will be echoed back by the server. The client will display hello world that is received from the server. The server will display the client's IP and the connection will be closed. 


## 3. ZeroMQ - High-level networking interface

* Our group acted as the publisher and this is the code 
* First install zmq and adafruit_bh1750 
```Python 
  # SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries

# SPDX-License-Identifier: Unlicense
import time
import zmq

import board

import adafruit_bh1750

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_bh1750.BH1750(i2c)



context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")


while True:
    #  Send reply back to client
    socket.send_string("%.2f Lux" % sensor.lux)
    
    time.sleep(1)

  ```
  
  