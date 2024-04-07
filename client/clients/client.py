import json
from interface import Interface
from sock import Sock

class Client:
    
    def __init__(self, interface: Interface) -> None:
        
        self.init = 0
        self.uuid = None
        
        self.interface = interface
        self.host = None
        self.current_packet = b""
        
        self.sock = Sock(verbose = True, client_type = "client")

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
    
    def on_init(self):
        self.sock.send_json({
            "type": "client"
        }) # init = 0
        print("[ CLIENT ] Init")
    
    def on_close(self):
        print("close")
    
    def send_packet(self):
        self.interface.send(self.current_packet)
        self.current_packet = b""
    
    def on_message(self, data):
        
        if self.init == 0:
            self.init = 1
            
            init_message = json.loads(data.decode("utf-8"))
            self.uuid = init_message["uuid"]
            print("[ CLIENT ] UUID: " + self.uuid)
            
            self.select_host(init_message["hosts"])
        else:
            print(".", end="", flush=True)
            self.data_type = data[0]
            self.packet = data[1:]
            
            if self.data_type == 0: # FULL PACKET
                self.current_packet = self.packet
                self.send_packet()
            elif self.data_type == 1: # PACKET START
                self.current_packet = self.packet
            elif self.data_type == 2: # PACKET CONTINUE
                self.current_packet += self.packet
            elif self.data_type == 3: # PACKET END
                self.current_packet += self.packet
                self.send_packet()