import socket
import json
import signal
from signal import Data
import pickle
import base64

target_addr = 'localhost'
target_port = 9999

print("hello")
#creating socket object

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_addr, target_port))
    #client = socket.create_connection((target_addr, target_port), source_address=('localhost', 9988))
    #connecting the client
    #sending data
    example = signal.Settings()
    messages =[]
    messages.append(b"PING")
    messages.append(b"ID,acquisition_1")
    messages.append(b"ENCODING,json")
    messages.append(b'DATA,' + json.dumps({'type':'Settings', 'data':example.__dict__}).encode())
    messages.append(b"ENCODING,pickle")
    messages.append(b'DATA,' + base64.b64encode(pickle.dumps(Data(example))))
    #messages.append(b"START_ACQUISITION,"+ base64.b64encode(pickle.dumps(Data(example))))
    for message in messages:
        client.send(message)
        #receiving the data 
        response = client.recv(1024)
        print(response.decode())
    #closing the connection
    #client.close()

    wait = input("Press Enter to continue...")

