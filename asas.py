import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG, format='%(threadName)s: %(message)s'
)

def thread1(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start1')
        time.sleep(1)
        logging.debug('end1')

def thread2(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start2')
        time.sleep(1)
        logging.debug('end2')

def thread3(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start3')
        time.sleep(1)
        logging.debug('end3')
def thread4(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start4')
        time.sleep(1)
        logging.debug('end4')

if __name__ == '__main__':
    barrier = threading.Barrier(2)
    t1 = threading.Thread(target=thread1, args=(barrier, ))
    t2 = threading.Thread(target=thread2, args=(barrier, ))
    t3 = threading.Thread(target=thread3, args=(barrier,))
    t4 = threading.Thread(target=thread4, args=(barrier,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()