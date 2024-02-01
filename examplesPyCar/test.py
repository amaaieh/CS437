import picar_4wd as fc
import time

while True:
    scan_list = fc.scan_step(15)
    if not scan_list:
        continue
    
    print(scan_list)
    
    tmp = scan_list[3:7]
    print(tmp)
    if tmp != [2,2,2,2]:
        time.sleep(3)
        fc.turn_right(speed)
    else:
        fc.forward(speed)