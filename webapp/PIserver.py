# Raspberry Pi server code
import socket

def start_server():
    host = ''  # Bind to all interfaces
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # You can process the received data here
                    data = data.decode()
                    #functionImake(data)
                    print("Received:", data)
                    conn.sendall(data)  # Echo back the received data

if __name__ == '__main__':
    start_server()



#functionImake{}
