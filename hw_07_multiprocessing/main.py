from multiprocessing import Process, Queue, Manager
import psutil
import random
import time


class ProcessPool:
    def __init__(self, min_workers=2, max_workers=10, mem_usage=1024):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.process_ram = 0

    def mem_test(self, func, data):
        shared_dict = Manager().dict()
        test_proc = Process(target=func, args=(data,))
        test_proc.start()
        proc_for_measure = Process(target=self.measure_ram, args=(test_proc.pid, shared_dict))
        proc_for_measure.start()
        test_proc.join()
        proc_for_measure.join()
        self.process_ram = shared_dict['process_ram']

    def measure_ram(self, pid, return_dict):
        max_ram = 0
        try:
            while psutil.pid_exists(pid):
                result = psutil.Process(pid).memory_info().rss / 1024 ** 2  # proc memory in MB
                if result > max_ram:
                    max_ram = result
        except psutil.NoSuchProcess:
            pass
        return_dict['process_ram'] = max_ram

    def map(self, func, big_data: Queue):
        self.mem_test(func, big_data.get())
        print("First process RAM: ", self.process_ram)
        if self.process_ram != 0:
            processes_number = int(self.mem_usage / self.process_ram)
        else:
            processes_number = self.max_workers
        print("Number of procs we can create: ", processes_number)
        data_size = big_data.qsize()
        print("Data size: ", data_size)
        procs = []

        if processes_number > self.max_workers:
            processes_number = self.max_workers
        elif processes_number < self.min_workers:
            raise Exception('Not enough memory!')

        for _ in range(processes_number):
            if not big_data.empty():
                proc = Process(target=func, args=(big_data.get(),))
                procs.append(proc)
                proc.start()

        while not big_data.empty():
            for idx, proc in enumerate(procs):
                if not proc.is_alive():
                    new_proc = Process(target=func, args=(big_data.get(),))
                    new_proc.start()
                    procs[idx] = new_proc
                    print('{0:.2f}%'.format(100 - (big_data.qsize() / data_size) * 100))

        for proc in procs:
            proc.join()

        print('All done')
        return len(procs), self.process_ram


def heavy_func(*args, **kwargs):
    array = [random.randint(0, 100) for _ in range(10000)]
    sorted(array)


if __name__ == '__main__':
    available_memory = psutil.virtual_memory().available / 1024 ** 2
    memory_to_use = available_memory * 0.7  # for additional security

    pool = ProcessPool(1, 100, memory_to_use)
    q = Queue()
    for _ in range(50):
        q.put(1)

    start = time.time()
    procs_number, first_proc_ram = pool.map(heavy_func, q)
    finish = time.time()

    print("Created processes number: ", procs_number)
    print("First process memory: ", first_proc_ram)
    print("Time: {0:.2f} s".format(finish - start))
