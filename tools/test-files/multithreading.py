import threading
import time
import queue
import random

class ThreadManager:
    def __init__(self, num_threads):
        self.threads = [{"thread": threading.Thread(target=self.worker), "is_busy": False} for _ in range(num_threads)]
        self.q = queue.Queue()
        self.stop_print_thread = threading.Event()
        self.print_thread = threading.Thread(target=self.print_results)
        self.print_thread.start()

    def worker(self, input): # Simulating the calculation
        x = {input: random.uniform(0, 10000)}
        time.sleep(4)
        self.q.put(x)

    def return_queue(self):
        if not self.q.empty():
            return self.q.get()
        return None

    def print_results(self):
        while not self.stop_print_thread.is_set():
            result = self.return_queue()
            if result is not None:
                print(result)
            time.sleep(0.5)

    def start_task(self, input):
        for t in self.threads:
            if not t["is_busy"]:
                t["thread"] = threading.Thread(target=self.worker, args=(input,))
                t["thread"].start()
                t["is_busy"] = True
                return True
        return False

    def check_threads(self):
        for t in self.threads:
            if not t["thread"].is_alive():
                t["is_busy"] = False

    def get_unused_threads(self):
        self.check_threads()
        return [t for t in self.threads if not t["is_busy"]]

tm = ThreadManager(5)
try:
    while True:
        inp = int(input("input: "))
        tm.start_task(inp)
        print("Unused threads:", len(tm.get_unused_threads()))
except KeyboardInterrupt:
    tm.stop_print_thread.set()