import socket 
import threading 
import json
import signal
import pickle
import base64
from types import SimpleNamespace
from enum import Enum

class Defaults:
    ENCODING = 'utf-8'
    PEER_TYPE = 'undefined'
    TAG = 'Undefined_Client'
    KEYWORD = 'NONE'
    DATA = 'NONE'

class RequestKeywords(Enum):
    PING = 'PING'
    ID = 'ID'
    DATA = 'DATA'
    ENCODING = 'ENCODING'
    SETTINGS = 'SETTINGS'
    START_ACQUISITION = 'START_ACQUISITION'

class Encoding(Enum):
    JSON = 'json'
    PICKLE = 'pickle'
    SNAP7 = 'snap7'
    UTF8 = 'utf-8'

class Responses(Enum):
    PONG = 'PONG'
    SETTINGS_RECEIVED = 'SETTINGS RECEIVED'
    DATA_RECEIVED = 'DATA RECEIVED'
    ENCODING_SET = 'ENCODING SET TO'
    ACQUISITION_STARTED = 'ACQUISITION STARTED'
    ERROR = 'ERROR'
    UNKNOWN_REQUEST = 'UNKNOWN REQUEST'
    ID = 'ID SET'

class PeerType(Enum):
    PLC = 'plc'
    GUI = 'gui'
    APP = 'app'
    ACQUISITION = 'acquisition'
    UNKNOWN = 'unknown'

class Session:
    encoding = 'utf-8'
    def __init__(self):
        pass

    def set_encoding(self, encoding):
        self.encoding = encoding

    def _get_json_data(self, raw_data):
        output = json.loads(raw_data, object_hook=lambda d: SimpleNamespace(**d))
        return output
    
    def _get_pickle_data(self, raw_data):
        output = pickle.loads(base64.b64decode(raw_data))
        return output

    def get_data(self, raw_data):
        print(f"[+] Decoding settings with encoding: {self.encoding}")
        print(f"[+] Raw data: {raw_data}")
        data = None
        match self.encoding:
            case Encoding.PICKLE.value:
                data = self._get_pickle_data(raw_data)
            case Encoding.JSON.value:    
                data = self._get_json_data(raw_data)
            case _:
                print("[!] Unknown encoding")
        print(f"[+] Data: {data.__dict__}")  
        return data
    
    def handle_request(self, request, client, mailbox):
        response = Request(receiver=client.tag)
        match request.keyword:
            case "PING":
                print(f"[+] Ping received from {client.addr}")
                response.set_keyword(Responses.PONG.value)
            case "ID":
                client.set_tag(request.data)
                print(f"[+] Client ID set to: {request.data}")
                response.set_keyword(Responses.ID.value)
            case "DATA":
                client.add_data(self.get_data(request.data))
                response.set_keyword(Responses.DATA_RECEIVED.value)
            case "ENCODING":
                self.set_encoding(request.data)
                print(f"[+] Encoding set to: {self.encoding}")
                response.set_keyword(Responses.ENCODING_SET.value)
                response.set_data(self.encoding)
            case "START_ACQUISITION":
                forward = Request(receiver_type=PeerType.ACQUISITION.value, keyword=request.keyword)
                if request.data is not None:
                    forward.set_data(self.get_data(request.data))
                else:
                    d = next((d for d in client.data if d.type == 'Settings'), Defaults.DATA)
                    forward.set_data(d)
                mailbox.append(forward)
                print(f"[+] Forwarding START_ACQUISITION to acquisition module")
                print(f"[+] Mailbox size: {len(mailbox)} | {[m.keyword for m in mailbox]} | {[m.receiver for m in mailbox]} | {[m.receiver_type for m in mailbox]}")
                response.set_keyword(Responses.ACQUISITION_STARTED.value)
            case _:
                print("[!] Unknown request")
                response.set_keyword(Responses.UNKNOWN_REQUEST.value)

        mailbox.append(response)
        print(f"[+] Response queued for {response.receiver}: {response.keyword} {response.data}")
        return
    
class Client:
    data = []
    def __init__(self, socket, addr):
        self.tag = Defaults.TAG
        self.peer_type = Defaults.PEER_TYPE
        self.socket = socket
        self.addr = addr
    def set_tag(self, tag):
        self.tag = tag
        if tag.find(PeerType.PLC.value) > -1:
            self.set_peer_type(PeerType.PLC.value)
        elif tag.find(PeerType.GUI.value) > -1:
            self.set_peer_type(PeerType.GUI.value)
        elif tag.find(PeerType.APP.value) > -1:
            self.set_peer_type(PeerType.APP.value)
        elif tag.find(PeerType.ACQUISITION.value) > -1:
            self.set_peer_type(PeerType.ACQUISITION.value)
        else:
            self.set_peer_type(PeerType.UNKNOWN.value)

    def set_peer_type(self, peer_type):
        self.peer_type = peer_type
    def add_data(self, data):
        self.data.append(data)
    
class Request:
    def __init__(self, receiver=Defaults.TAG, receiver_type=Defaults.PEER_TYPE, keyword=Defaults.KEYWORD, data=None, encoding=Defaults.ENCODING):
        self.receiver = receiver
        self.receiver_type = receiver_type
        self.keyword = keyword
        self.data = data
        self.encoding = encoding
    def set_encoding(self, encoding):
        self.encoding = encoding
    def set_keyword(self, keyword):
        self.keyword = keyword
    def set_data(self, data):
        self.data = data
    def set_receiver_type(self, receiver_type):
        self.receiver_type = receiver_type
    def set_receiver(self, receiver):
        self.receiver = receiver
    
#mailbox handling thread
def handle_mailbox(mailbox): 
    for message in mailbox:
        print(f"[MAILBOX] To: {message.receiver} | Type: {message.receiver_type} | Keyword: {message.keyword} | Data: {message.data}")


#client handling thread
def handle_client(c, mailbox ): 
    session = Session()
    while True:
        #printing what the client sends
        try:
            c.socket.settimeout(10)
            buffer = c.socket.recv(1024)
        except socket.timeout:
            print(f"[-] Client {c.tag} timed out")
            break
        if not buffer:
            print(f"[-] Client {c.tag} disconnected")
            break
        request = Request()
        request.keyword, s, request.data = buffer.decode().partition(',')
        print(f"[+] Recieved: {buffer}") 
        session.handle_request( request, c, mailbox)
        #sending response, if any
        resp = next((r for r in mailbox if r.receiver == c.tag and r.receiver != Defaults.TAG or r.receiver_type == c.peer_type), Request())
        if resp in mailbox:
            mailbox.remove(resp)
        c.socket.send(resp.keyword.encode() + (b',' + str(resp.data).encode() if resp.data is not None else b''))
        #client_socket.close()
    c.socket.close()

mailbox = []
clients = []

# localhost
bind_ip = "0.0.0.0" 
bind_port = 9999

server = socket.create_server((bind_ip, bind_port))
# we tell the server to start listening with 
# a maximum backlog of connections set to 5
server.listen(5) 
print(f"[+] Listening on port {bind_ip} : {bind_port}")                            


while True: 
    # When a client connects we receive the 
    # client socket into the client variable, and 
    # the remote connection details into the addr variable
    c_sock, addr = server.accept() 
    print(f"[+] Connection established from: {addr[0]}:{addr[1]} | Socket: {c_sock}")
    print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
    # enlist client
    c = next((cl for cl in clients if cl.socket == c_sock or cl.addr == addr ), None)
    if c is None:
        c_rec = Client(socket=c_sock, addr=addr)
        clients.append(c_rec)
        c = c_rec    
    print(f"[+] Listed clients: {len(clients)}")
    print(f"[+] Client list: {[cl.addr for cl in clients]} | {[cl.tag for cl in clients]} | {[cl.peer_type for cl in clients]}")
    # spin up our client thread to handle the incoming data 
    client_handler = threading.Thread(target=handle_client, args=(c, mailbox))
    client_handler.start() 
    # handle the response
    # start mailbox handler thread
    if len(mailbox) > 0 and not any(t.name == "mailbox_handler" for t in threading.enumerate()):
        mailbox_handler = threading.Thread(target=handle_mailbox, args=(mailbox,))  
        mailbox_handler.start()


        
