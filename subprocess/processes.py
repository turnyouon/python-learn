import multiprocessing
import time


def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1


if __name__ == "__main__":
    p = multiprocessing.Process(target=worker, args=(3,))
    p.start()
    p2 = multiprocessing.Process(target=worker, args=(2,))
    p2.start()
    print "p.pid:", p.pid
    print "p.name:", p.name
    print "p.is_alive:", p.is_alive()
    print "p.pid:", p2.pid
    print "p.name:", p2.name
    print "p.is_alive:", p2.is_alive()