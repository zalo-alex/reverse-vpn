import json
from interface import Interface
from sock import Sock
from utils import handle_packet_chunk, send_packet_to_sock

class Client:
    
    def __init__(self, interface: Interface, host = "127.0.0.1", port = 16782) -> None:
        
        self.init = 0
        self.uuid = None
        
        self.interface = interface
        
        self.interface.on_packet = self.on_packet
        
        self.host = None
        self.current_packet = b""
        
        self.sock = Sock(host, port, verbose = True, client_type = "client")

        self.sock.on_init = self.on_init
        self.sock.on_close = self.on_close
        self.sock.on_message = self.on_message

        self.sock.start(thread = False) # Blocked here.
    
    def select_host(self, hosts):
        print("[ CLIENT ] Hosts:")
        
        for i, host in enumerate(hosts):
            print(f"[ CLIENT ] {i}\t" + host)
            
        host = input("[ CLIENT ] > ")
        self.host = hosts[int(host)]
        
        self.sock.send_json({
            "host": self.host
        }) # init = 1
    
    def on_packet(self, data, raw, timestamp, is_self):
        if not is_self:
            return
        
        send_packet_to_sock(self.sock, raw)
        
    def on_init(self):
        self.sock.send_json({
            "type": "client"
        }) # init = 0
        print("[ CLIENT ] Init")
    
    def on_close(self):
        print("close")
    
    def on_message(self, data):
        
        if self.init == 0:
            self.init = 1
            
            init_message = json.loads(data.decode("utf-8"))
            self.uuid = init_message["uuid"]
            print("[ CLIENT ] UUID: " + self.uuid)
            
            self.select_host(init_message["hosts"])
        else:
            print("!", end="", flush=True)
            handle_packet_chunk(self, data)