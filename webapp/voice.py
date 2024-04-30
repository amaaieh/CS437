from random import randint
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import keyboard
  
# https://github.com/knucklesuganda/twisted_voice_chat/blob/master/main.py


class Client(DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.isPi = True

    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = 1024  # 127.0.0.1
        self.another_client = "10.0.0.220", 2222
        self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                           output=True, rate=16000, channels=1,
                                           frames_per_buffer=self.buffer)
        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True, rate=16000, channels=1,
                                          frames_per_buffer=self.buffer)
        reactor.callInThread(self.record)
#10.1.11.253
    def record(self):
        while True:
            if self.isPi or keyboard.is_pressed('t'):
                data = self.input_stream.read(self.buffer, exception_on_overflow=False)
                self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, addr):
        self.output_stream.write(datagram)

    def toggleIsPi(self):
        self.isPi = not self.isPi


if __name__ == '__main__':
    port = 2222
    print("Working on port: ", port)
    cli = Client()
    cli.toggleIsPi()  # Defaults to true
    reactor.listenUDP(port, cli)
    reactor.run()
