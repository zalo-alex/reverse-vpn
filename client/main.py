import argparse

from clients.client import Client
from clients.host import HostClient
from interface import Interface

def main(host, port, client_type, interface_name=None):
    
    if client_type == "c":
        Interface.show_ifnames()
        
        if interface_name is None:
            interface_name = input("Interface name: ")
            
        client = Client(Interface(interface_name), host, port)
        
    elif client_type == "h":
        Interface.show_ifnames()
        
        if interface_name is None:
            interface_name = input("Interface name: ")
            
        client = HostClient(Interface(interface_name), host, port)
        
    else:
        print("Invalid client type")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client configuration")
    parser.add_argument("host", type=str, help="Host")
    parser.add_argument("port", type=int, help="Port")
    parser.add_argument("client_type", choices=["c", "h"], help="Client type (c/h)")
    parser.add_argument("--interface", "-i", type=str, help="Interface name")

    args = parser.parse_args()

    main(args.host, args.port, args.client_type, args.interface)
