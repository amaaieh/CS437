import picar_4wd as fc
import time

def forwardX(x):
    fc.forward(50)
    time.sleep(.6 * x)
    fc.stop()

def backwardX(x):
    fc.backward(50)
    time.sleep(.6 * x)
    fc.stop()

def turn180():
    fc.turn_right(50)
    time.sleep(2.8)
    fc.stop()

def turnRight90():
    fc.turn_right(50)
    time.sleep(1.4)
    fc.stop()

def turnLeft90():
    fc.turn_left(50)
    time.sleep(1.4)
    fc.stop()

forwardX(1)
time.sleep(1)
turn180()
time.sleep(1)
turnRight90()
time.sleep(1)
backwardX(2)
time.sleep(1)
turnLeft90()
time.sleep(1)
forwardX(3)