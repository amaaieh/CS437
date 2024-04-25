import socket
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))  # Replace SERVER_IP_ADDRESS with the server's IP address

audio = pyaudio.PyAudio()

stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

while True:
    try:
        data = stream_in.read(CHUNK)
        client_socket.sendall(data)
        data = client_socket.recv(CHUNK)
        stream_out.write(data)
    except KeyboardInterrupt:
        break

print("Closing connection...")
stream_out.stop_stream()
stream_out.close()
stream_in.stop_stream()
stream_in.close()
audio.terminate()
client_socket.close()
