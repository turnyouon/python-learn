import multiprocessing
import time

def wait_for_event(e):
    print("wait_for_event: starting")
    e.wait()
    print("wairt_for_event: e.is_set()->" + str(e.is_set()))

def wait_for_event_timeout(e, t):
    print("wait_for_event_timeout:starting")
    e.wait(t)
    print("wait_for_event_timeout:e.is_set->" + str(e.is_set()))

if __name__ == "__main__":
    e = multiprocessing.Event()

    for i in range(1, 10000):
        w = multiprocessing.Process(name = "block",
            target = wait_for_event,
            args = (e,))

        w.start()

        x

    e.set()
    print("main: event is set")