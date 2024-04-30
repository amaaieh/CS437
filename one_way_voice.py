from random import randint
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import keyboard
import argparse


class Client(DatagramProtocol):
    def __init__(self, ip_address):
        super().__init__()
        self.isPi = True
        self.ip_address = ip_address

    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = 1024  # 127.0.0.1
        self.another_client = (self.ip_address, 2222)

        self.input_stream = py_audio.open(
            input_device_index=1,
            format=pyaudio.paInt16,
            input=True,
            rate=16000,
            channels=1,
            frames_per_buffer=self.buffer,
        )
        reactor.callInThread(self.record)

    def record(self):
        while True:
            if self.isPi or keyboard.is_pressed("t"):
                # print(self.isPi, keyboard.is_pressed('t'))
                data = self.input_stream.read(self.buffer, exception_on_overflow=False)
                self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, addr):
        pass

    def toggleIsPi(self):
        self.isPi = not self.isPi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--ip",
        help="IP address of the destination client.",
        required=False,
        type=str,
        default="10.3.161.69",
    )
    args = parser.parse_args()

    port = 2222
    print("Working on port: ", port)
    cli = Client(args.ip)
    reactor.listenUDP(port, cli)
    reactor.run()
