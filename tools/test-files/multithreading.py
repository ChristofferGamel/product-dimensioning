import threading
import time
import queue

class ThreadManager:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.semaphore = threading.Semaphore(num_threads)

    def start_task(self, inp):
        self.task_queue.put(inp)
        while not self.task_queue.empty():
            for _ in range(self.num_threads):
                if self.semaphore.acquire(blocking=False):  # Try acquiring without blocking
                    threading.Thread(target=self.worker).start()
                else:
                    time.sleep(0.1)  # If no semaphore available, sleep a bit

    def worker(self):
        try:
            input = self.task_queue.get()
            x = {input: input}
            time.sleep(4)
            print(x) 
        finally:  # To ensure the semaphore is always released, even if an exception occurs
            self.semaphore.release()

    def threads_amount(self):
        return self.semaphore._value

tm = ThreadManager(2)
try:
    while True:
        print("Unused threads1:", tm.threads_amount())
        inp = int(input("input: "))
        tm.start_task(inp)
        print("Unused threads2:", tm.threads_amount())

except KeyboardInterrupt:
    pass  # This will just exit the loop and end the program. `tm.stop()` method does not exist in the provided code.
