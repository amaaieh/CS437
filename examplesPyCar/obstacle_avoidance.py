import picar_4wd as fc
import random 
import time

speed = 30
def backwardX(x):
    fc.backward(50)
    time.sleep(.6 * x)
    fc.stop()

def main():
    while True:
        scan_list = fc.scan_step(15)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            backwardX(1)
            random_number = random.randint(1, 2)
            if(random_number == 1):
                fc.turn_right(speed)
                time.sleep(1)
            else: 
                fc.turn_left(speed)
                time.sleep(1)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
