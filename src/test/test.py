import threading
import time

def th1():
    while True:
        print('th1')
        time.sleep(0.5)

def th2():
    while True:
        print('th2')
        time.sleep(0.5)

if __name__ == '__main__':
    thr1 = threading.Thread(target=th1)
    thr2 = threading.Thread(target=th2)
    thr1.start()
    thr2.start()
    # thr1.join()
    # thr2.join()