import picar_4wd as fc
import sys
import tty
import termios
import asyncio
import time

power_val = 50

def command_response(data):
    if data == 'lock':
        fc.forward(power_val)
        time.sleep(0.5)
        fc.stop()
    elif data == 'unlock':
        fc.backward(power_val)
        time.sleep(0.5)
        fc.stop()
    return None
