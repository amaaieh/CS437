import picar_4wd as fc
import time

def forwardX(x):
    fc.forward(10000)
    time.sleep(.6 * x)
    fc.stop()

def backwardX(x):
    fc.backward(50)
    time.sleep(.6 * x)
    fc.stop()

def turn180():
    fc.turn_right(50)
    time.sleep(2.15)
    fc.stop()

def turnRight90():
    fc.turn_right(20)
    time.sleep(1.5)
    fc.stop()

def turnLeft90():
    fc.turn_left(50)
    time.sleep(1.35)
    fc.stop()