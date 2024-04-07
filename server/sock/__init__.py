import socket
import threading

from sock.client import Client

class Sock:
    
    HOSTS = {}
    CLIENTS = {}
    
    def __init__(self, host = '127.0.0.1', port = 8080, verbose = False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        
        self.verbose = verbose
        self.sock = sock
        
        self.log('Sock created and bind to ' + host + ':' + str(port))
    
    def log(self, msg):
        if self.verbose: print(msg)
    
    def listen(self):
        self.sock.listen()
        self.log('Server is listening on ' + self.sock.getsockname()[0] + ':' + str(self.sock.getsockname()[1]))
        
        while True:
            sock, addr = self.sock.accept()
            self.new_client(sock, addr)
    
    def new_client(self, sock, addr):
        client = Client(self, sock, addr)
        client.handle()
    
    def start(self, thread):
        if thread:
            threading.Thread(target=self.listen).start()
        else:
            self.listen()
    
    def __exit__(self, type, value, traceback):
        self.sock.close()