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
            queue_size = self.task_queue.qsize()            
            if self.task_queue.qsize() > self.num_threads:
                self.start_workers(self.num_threads)
            else:
                self.start_workers(queue_size)

    def start_workers(self, threads_amount):
        for _ in range(threads_amount): 
            if self.semaphore.acquire(blocking=False):
                threading.Thread(target=self.worker).start()
            else:
                time.sleep(0.1)

    def worker(self):
        try:
            input = self.task_queue.get()
            print(f"Worker: {threading.get_ident()}, Working on task: {input}")
            x = {input: input}
            time.sleep(4)
            print(x) 
        finally: 
            self.semaphore.release()
            print("Threads after executing:", self.threads_amount())

    def threads_amount(self):
        return self.semaphore._value

tm = ThreadManager(2)
try:
    while True:
        inp = int(input("input: "))
        tm.start_task(inp)
        print("Unused threads:", tm.threads_amount())

except KeyboardInterrupt:
    pass
