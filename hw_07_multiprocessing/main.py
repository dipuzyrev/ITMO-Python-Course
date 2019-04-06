from multiprocessing import Process, Queue, Manager
import psutil
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
                time.sleep(1)
        except psutil.NoSuchProcess:
            pass
        return_dict['process_ram'] = max_ram

    def map(self, func, data):

        big_data = Queue()
        for i in range(len(data)):
            big_data.put(data[i])

        self.mem_test(func, big_data.get())
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
                    print('process #{0:d} done ({1:.2f}%)'.format(proc.pid, 100 - (big_data.qsize() / data_size) * 100))
                    new_proc = Process(target=func, args=(big_data.get(),))
                    new_proc.start()
                    procs[idx] = new_proc

        for proc in procs:
            proc.join()

        print('All done')
        return len(procs), self.process_ram
