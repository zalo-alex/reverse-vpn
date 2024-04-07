from interface import Interface
        
if __name__ == "__main__":
    client_type = input("Client type (c/h): ")
    
    if client_type == "c":
        from clients.client import Client
        
        Interface.show_ifnames()
        
        client = Client(
            Interface("Famatech Radmin VPN Ethernet Adapter") #input("Interface name: "))
        )
    elif client_type == "h":
        from clients.host import HostClient
        
        Interface.show_ifnames()
        
        client = HostClient(
            Interface("Realtek Gaming GbE Family Controller") #input("Interface name: "))
        )
    else:
        print("Invalid client type")
        exit(1)