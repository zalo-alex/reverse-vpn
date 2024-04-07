from scapy.all import *
from scapy.layers.l2 import Ether

class Interface:
    
    def __init__(self, ifname = "eth0") -> None:
        self.ifname = ifname
        self.iface = IFACES.dev_from_name(ifname)
        self.socket = conf.L2socket(iface=self.iface)
        self.mac = get_if_hwaddr(ifname)
        
        self.on_packet = None
    
    def send(self, payload):
        self.socket.send(payload)
    
    def _listen(self):
        while True:
            packet = self.socket.recv_raw()
            
            if self.on_packet and packet[0]:
                src_mac = Ether(packet[1]).src
                self.on_packet(packet[0], packet[1], packet[2], src_mac == self.mac)
    
    def listen(self, thread = True):
        if thread:
            threading.Thread(target=self._listen).start()
        else:
            self._listen()
    
    @staticmethod
    def show_ifnames():
        IFACES.show()

# iface = IFACES.dev_from_name(r"Hyper-V Virtual Ethernet Adapter #2")
# socket = conf.L2socket(iface=iface)
# # socket is now an Ethernet socket
# ### RECV
# last_packet = None
# while True:
#     packet_raw = socket.recv_raw()[1]  # Raw data
#     if packet_raw and last_packet != packet_raw:
#         print(packet_raw)
#         socket.send(packet_raw)
#         last_packet = packet_raw

# packet_decoded = socket.recv() # Using the library (also contains things like sent time...)
# print(packet_decoded)
# ### SEND
# #socket.send(b"\x00......"). # send raw data
# #socket.send(Ether()/IP(dst="www.google.com")/TCP()/Raw(load=b"data")) # use library
