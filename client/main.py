from interface import Interface
        
if __name__ == "__main__":
    host = input("Host: ")
    port = input("Port: ")
    client_type = input("Client type (c/h): ")
    
    if client_type == "c":
        from clients.client import Client
        
        Interface.show_ifnames()
        
        client = Client(
            Interface(input("Interface name: ")),
            host,
            port
        )
    elif client_type == "h":
        from clients.host import HostClient
        
        Interface.show_ifnames()
        
        client = HostClient(
            Interface(input("Interface name: ")),
            host,
            port
        )
    else:
        print("Invalid client type")
        exit(1)