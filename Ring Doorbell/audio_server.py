import socket
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5555))
server_socket.listen(5)
print("Server listening...")

connection, client_address = server_socket.accept()
print(f"Connection from {client_address}")

audio = pyaudio.PyAudio()

stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

while True:
    try:
        data = connection.recv(CHUNK)
        stream_out.write(data)
        data = stream_in.read(CHUNK)
        connection.sendall(data)
    except KeyboardInterrupt:
        break

print("Closing connection...")
stream_out.stop_stream()
stream_out.close()
stream_in.stop_stream()
stream_in.close()
audio.terminate()
connection.close()
server_socket.close()
