import json
import threading
import uuid

class Client:
    
    def __init__(self, server, sock, addr) -> None:
        self.server = server
        self.sock = sock
        self.addr = addr
        self.type = None
        self.uuid = str(uuid.uuid4())
        self.init = 0
        
        # Client
        self.selected_host = None
        
        # Host
        self.clients = []
    
    def send(self, data):
        self.sock.send(data)
    
    def send_json(self, data):
        self.send(json.dumps(data).encode("utf-8"))
    
    def load_init_data(self, data):
        self.init_message = json.loads(data.decode())
        
        if self.init == 0:
            self.type = self.init_message['type']
            self.init = 1
            
            res_data = {
                "uuid": self.uuid
            }
            
            if self.type == "host":
                self.server.HOSTS[self.uuid] = self
            else:
                self.server.CLIENTS[self.uuid] = self
                res_data["hosts"] = list(self.server.HOSTS.keys())
            
            self.send_json(res_data)
            
        elif self.init == 1:
            self.selected_host = self.init_message['host']
            self.server.HOSTS[self.selected_host].clients.append(self)
            self.init = 2
        
        if self.type == "host":
            self.init = 2
    
    def send_to_clients(self, data):
        for client in self.clients:
            print(".", end="", flush=True)
            client.send(data)

    def _handle(self):
        try:
            while True:
                data = self.sock.recv(4096)
                
                if self.init < 2:
                    self.load_init_data(data)
                elif self.type == "host":
                    print(":", end="", flush=True)
                    self.send_to_clients(data)
                    
        except:
            if self.type == "client":
                self.server.HOSTS[self.selected_host].clients.remove(self)
    
    def handle(self):
        threading.Thread(target=self._handle).start()