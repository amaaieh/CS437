from vidstream import StreamingServer
from vidstream import AudioSender
from vidstream import AudioReceiver
import threading
import socket
import time

ip = "127.0.0.1"

server = StreamingServer(ip, 9999)


server.start_server()

receiver = AudioReceiver(ip, 5555)
receive_thread = threading.Thread(target=receiver.start_server)
receive_thread.start()

time.sleep(5)
sender = AudioSender(ip, 5554)
sender_thread = threading.Thread(target=sender.start_stream)
sender_thread.start()

print("Server started")
# Other Code

# When You Are Done
#server.stop_server()