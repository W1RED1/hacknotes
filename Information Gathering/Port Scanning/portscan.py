import sys
import time
import socket
import threading
from queue import Queue

class Worker():
        def __init__(self, target, timeout):
                self.target = target
                self.timeout = timeout
                self.queue = Queue()

        def scan(self):
                while 1:
                        port = self.queue.get()
                        if port == None:
                                return

                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.settimeout(self.timeout)
                        result = s.connect_ex((self.target, port))
                        if result == 0:
                                print("Port %s: open" %(port))

                        s.close()

        def start(self):
                self.thread = threading.Thread(target=self.scan)
                self.thread.start()

        def join(self):
                self.thread.join()

if __name__ == '__main__':
        if len(sys.argv) != 6 or '-h' in sys.argv or '--help' in sys.argv:
                print("usage: ./prog [TARGET] [START PORT] [STOP PORT] [TIMEOUT (seconds)] [THREAD COUNT]")
                sys.exit()

        target  = sys.argv[1]
        start   = int(sys.argv[2])
        stop    = int(sys.argv[3])
        timeout = float(sys.argv[4])
        threads = int(sys.argv[5])

        print("Initiating scan against target %s..." %(target))
        clock = time.time()
        workers = []

        # spawn workers
        for i in range(threads):
                worker = Worker(target, timeout)
                worker.start()
                workers.append(worker)

        # send jobs to workers until exhausted
        ports = iter(range(start, stop+1))
        while 1:
                port = next(ports, None)
                if port == None:
                        break

                worker = workers.pop(0)
                worker.queue.put(port)
                workers.append(worker)

        # collect workers
        [worker.queue.put(None) for worker in workers]
        [worker.join() for worker in workers]
        duration = time.time() - clock
        print("\nTime elapsed: %s seconds" %(duration))
