import json
import threading
from utils import handle_packet_chunk, send_packet_to_sock
from sock import Sock
from interface import Interface

class HostClient:
    
    def __init__(self, interface: Interface, host = "127.0.0.1", port = 16782) -> None:
        
        self.interface = interface
        
        self.interface.on_packet = self.on_packet
        
        self.init = 0
        self.uuid = None
        
        self.sock = Sock(host, port, verbose = True, client_type = "host")

        self.sock.on_init = self.on_init
        self.sock.on_close = self.on_close
        self.sock.on_message = self.on_message

        self.sock.start(thread = False) # Blocked here.
    
    def on_packet(self, data, raw, timestamp, is_self):
        if is_self:
            return
        
        send_packet_to_sock(self.sock, raw)
    
    def on_init(self):
        self.sock.send_json({
            "type": "host"
        }) # init = 0
        print("[ HOST ] Init")
    
    def on_close(self):
        print("close")
    
    def on_message(self, data):
        
        if self.init == 0:
            self.init = 1
            
            init_message = json.loads(data.decode("utf-8"))
            self.uuid = init_message["uuid"]
            print("[ HOST ] UUID: " + self.uuid)
            threading.Thread(target=self.interface.listen).start()
            return
        
        print("!", end="", flush=True)
        handle_packet_chunk(self, data, True)
