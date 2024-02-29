import socket
#from picar_4wd import utils

HOST = "10.0.101.6" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)     
                client.sendall("this is something different (Battery, Position, and Distance traveled)") # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    