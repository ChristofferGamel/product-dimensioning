import threading
import time
import queue
import random

class ThreadManager:
    def __init__(self, num_threads):
        self.threads = [{"thread": threading.Thread(target=self.worker), "is_busy": False} for _ in range(num_threads)]
        self.q = queue.Queue()
        self.chain = QueueManager()
        self.stop_print_thread = threading.Event()
        self.print_thread = threading.Thread(target=self.print_results)
        self.print_thread.start()

    def worker(self, input): # Simulating the calculation
        x = {input: input}
        time.sleep(4)
        self.q.put(x)

    def return_queued_value(self):
        if not self.q.empty():
            return self.q.get()
        return None

    def print_results(self):
        while not self.stop_print_thread.is_set():
            result = self.return_queued_value()
            if result is not None:
                print(result)
            time.sleep(0.5)
    
    def queued_items(self):
        length_of_queue = self.chain.queue_length()
        if length_of_queue == 0:
            return False
        elif length_of_queue > 0:
            return True
        
    def start_task(self, input):
        self.chain.add_to_queue(input)
        chain_length = self.chain.queue_length()
        while chain_length > 0:
            # threads = self.check_threads()
            # if threads != None:
            #     threads["thread"] = threading.Thread(target=self.worker, args=(self.chain.get_first(),))
            #     threads["thread"].start()
            #     threads["is_busy"] = True
            for t in self.threads:
                if not t["is_busy"]:
                    t["thread"] = threading.Thread(target=self.worker, args=(self.chain.get_first(),))
                    t["thread"].start()
                    t["is_busy"] = True
                    return True
            return False
        
        


    def check_threads(self):
        for t in self.threads:
            if t["thread"].is_alive():
                t["is_busy"] = True
                return
            else: 
                return t

    def threads_amount(self):
        self.check_threads()
        return [t for t in self.threads if not t["is_busy"]]

class QueueManager():
    def __init__(self) -> None:
        self.queue = []
        pass

    def add_to_queue(self, val):
        self.queue.append(val)
    
    def get_first(self):
        first_element = self.queue[0]
        self.remove_from_queue(first_element)
        return first_element
    
    def remove_from_queue(self, element): # Internal Class function
        self.queue.remove(element)
        
    def queue_length(self):
        return len(self.queue)

tm = ThreadManager(2)
try:
    while True:
        inp = int(input("input: "))
        tm.start_task(inp)
        print("Unused threads:", len(tm.threads_amount()))
except KeyboardInterrupt:
    tm.stop_print_thread.set()