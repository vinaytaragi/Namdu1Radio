import os
import socket

local_server = "192.168.1."

def is_connected(network):
    try:
        #if ".com" in network:
        #    network = socket.gethostbyname(network)
        s = socket.create_connection((network, 80))
        return True
    except:
        return False
    
for server in range(50,251):
    if is_connected(local_server+str(server)):
        print("local server detected:",local_server+str(server))
    