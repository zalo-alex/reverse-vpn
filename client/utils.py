from scapy.layers.l2 import Ether

def send_packet_to_sock(sock, raw):
    chunk_size = sock.CHUNK_SIZE - 1
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
            
        print(".", end="", flush=True)
        
        sock.send(chunk)

def handle_packet_chunk(client, chunk, mac = False):
    client.data_type = chunk[0]
    client.packet = chunk[1:]
    
    if client.data_type == 0: # FULL PACKET
        client.current_packet = client.packet
        send_packet(client, mac)
        
    elif client.data_type == 1: # PACKET START
        client.current_packet = client.packet
        
    elif client.data_type == 2: # PACKET CONTINUE
        client.current_packet += client.packet
        
    elif client.data_type == 3: # PACKET END
        client.current_packet += client.packet
        send_packet(client, mac)

def send_packet(client, mac = False):
    
    if mac:
        pkt = Ether(client.current_packet)
        pkt.src = client.interface.mac
        client.current_packet = pkt.build()
    
    client.interface.send(client.current_packet)
    client.current_packet = b""