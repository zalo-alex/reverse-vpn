import json
import socket
import threading

class Sock:
    
    CHUNK_SIZE = 4096
    
    def __init__(self, host = '127.0.0.1', port = 16782, verbose = False, client_type = "client"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        self.verbose = verbose
        self.sock = sock
        
        self.on_init = None
        self.on_message = None
        self.on_close = None
        
        self.log('Sock created and connected to ' + host + ':' + str(port))
    
    def log(self, msg):
        if self.verbose: print(msg)
    
    def send(self, data):
        self.sock.sendall(data)
    
    def send_json(self, data):
        self.send(json.dumps(data).encode("utf-8"))
    
    def recv(self):
        if self.on_init:
            self.on_init()
        
        while True:
            data = self.sock.recv(1024)
            
            if self.on_message:
                self.on_message(data)
    
    def start(self, thread):
        if thread:
            threading.Thread(target=self.recv).start()
        else:
            self.recv()
    
    def __exit__(self, type, value, traceback):
        self.sock.close()
        
        if self.on_close:
            self.on_close()