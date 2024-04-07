import json
import threading
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
    
    def send_packet(self, raw):
        chunk_size = self.sock.CHUNK_SIZE - 1
        chunks = [ raw[ i:i + chunk_size ] for i in range(0, len(raw), chunk_size) ]
        
        for i, chunk in enumerate(chunks):
            
            if len(chunks) == 1:
                chunk = b"\x00" + chunk
            elif i == 0:
                chunk = b"\x01" + chunk
            elif i == len(chunks) - 1:
                chunk = b"\x03" + chunk
            else:
                chunk = b"\x02" + chunk
                
            #print(len(chunk), "(", i + 1, "/", len(chunks), ")\n", chunk)
            print(".", end="", flush=True)
            
            self.sock.send(chunk)
    
    def on_packet(self, data, raw, timestamp, is_self):
        if is_self:
            return
        
        self.send_packet(raw)
    
    def on_init(self):
        threading.Thread(target=self.interface.listen).start()
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
