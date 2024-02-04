import picar_4wd as fc
import time

def forwardX(x):
    fc.forward(15)
    time.sleep(.5 * x)
    fc.stop()

def backwardX(x):
    fc.backward(50)
    time.sleep(.6 * x)
    fc.stop()

def turn180():
    fc.turn_right(50)
    time.sleep(2.03)
    fc.stop()

def turnRight90():
    fc.turn_right(48)
    time.sleep(1.0)
    fc.stop()

def turnLeft90():
    time.sleep(0.2)
    fc.turn_left(65)
    time.sleep(1.17)
    fc.stop()
    fc.forward(15)
    time.sleep(0.5)
    fc.stop()
    time.sleep(2)

