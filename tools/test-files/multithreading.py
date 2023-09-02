import threading
import time
import queue

class ThreadManager:
    def __init__(self, num_threads):
        self.task_queue = queue.Queue()
        self.chain = QueueManager()
        self.semaphore = threading.Semaphore(num_threads)
        self.active = True

        for _ in range(num_threads):
            threading.Thread(target=self.worker).start()

    def worker(self):  # Simulating the calculation
        while self.active or not self.task_queue.empty():
            input = self.task_queue.get()
            if input is None:
                break

            x = {input: input}
            time.sleep(4)
            print(x)
            self.semaphore.release()

    def start_task(self, input):
        self.chain.add_to_queue(input)
        self.assign_tasks()

    def assign_tasks(self):
        while not self.chain.queue_is_empty() and self.semaphore.acquire(blocking=False):
            task = self.chain.get_first()
            self.task_queue.put(task)

    def threads_amount(self):
        return self.semaphore._value

    def stop(self):
        self.active = False


class QueueManager():
    def __init__(self) -> None:
        self.queue = []

    def add_to_queue(self, val):
        self.queue.append(val)

    def get_first(self):
        first_element = self.queue.pop(0)
        return first_element

    def queue_is_empty(self):
        return len(self.queue) == 0


tm = ThreadManager(2)
try:
    while True:
        inp = int(input("input: "))
        tm.start_task(inp)
        print("Unused threads:", tm.threads_amount())
except KeyboardInterrupt:
    tm.stop()
