import socket
from picar_4wd import utils
import controls


HOST = "10.0.101.6" # IP address of your Raspberry PI
PORT = 65445          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                command = data.decode()
                print(command)
                print(type(command))
                if(command == "left"):
                    controls.turnLeft()
                elif(command == "right"):
                    controls.turnRight()
                elif(command == "forward"):
                    controls.forward()
                elif(command == "backward"):
                    controls.backward()
                else:
                    controls.stop()
                # print(data)     
                result = utils.pi_read()
                #print(type(result["battery"]))
                client.sendall(str(result["battery"]) + ";" + str(result["cpu_temperature"]) + ";" + str(result["cpu_usage"]).encode()) # Echo back to client

    except: 
        print("Closing socket")
        client.close()
        s.close()    
