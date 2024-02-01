import picar_4wd as fc
import time

speed = 25
redirect_speed = 10
stop_time = 3
reverse_time = 1
turning_time = 3

scanDist = 35


def redirect():
    fc.stop()
    time.sleep(stop_time)
    fc.backward(redirect_speed)
    time.sleep(reverse_time)
    fc.turn_right(redirect_speed)
    time.sleep(turning_time)

def completeScan():
    scan_list = fc.scan_step(scanDist)
    while not scan_list or len(scan_list) != 10:
        scan_list = fc.scan_step(scanDist)
    
    return scan_list[3:7]

position = 0
while True:
    
    tmp = completeScan()
    print(tmp)
    while tmp != [2,2,2,2]:
        redirect()
        tmp = completeScan()
    else:
        fc.forward(speed)