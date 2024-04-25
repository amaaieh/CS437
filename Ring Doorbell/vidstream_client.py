from vidstream import CameraClient
from vidstream import VideoClient
from vidstream import ScreenShareClient

from vidstream import StreamingServer
from vidstream import AudioSender
from vidstream import AudioReceiver
import threading
import socket
import time

# Choose One
ip = "127.0.0.1"

client1 = CameraClient(ip, 9999)


client1.start_stream()


sender = AudioSender(ip, 5555)
sender_thread = threading.Thread(target=sender.start_stream)
sender_thread.start()

time.sleep(5)

receiver = AudioReceiver(ip, 5554)
receive_thread = threading.Thread(target=receiver.start_server)
receive_thread.start()


print("Stream started")