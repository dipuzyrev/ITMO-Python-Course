import unittest
import time
import random
from main import *
import sys
import gc


def heavy_func(*args, **kwargs):
    array = [random.randint(0, 100) for _ in range(100000)]
    sorted(array)
    array.clear()
    del array
    gc.collect()
    time.sleep(1)
    array = [random.randint(0, 100) for _ in range(200000)]
    sorted(array)
    array = [random.randint(0, 100) for _ in range(100)]
    sorted(array)


class TestProcessesWork(unittest.TestCase):

    def test_process_pool(self):
        data = [_ for _ in range(10)]

        print("RUNNING WITHOUT POOL:")
        start = time.time()

        for _ in data:
            heavy_func()

        finish = time.time()
        time1 = finish - start
        print("Time: {0:.2f} s\n".format(time1))

        available_memory = psutil.virtual_memory().available / 1024 ** 2
        memory_to_use = available_memory * 0.8  # for additional security

        pool = ProcessPool(2, 100, memory_to_use)

        start = time.time()
        procs_number, first_proc_ram = pool.map(heavy_func, data)
        finish = time.time()
        time2 = finish - start

        print("\nUSING POOL:")
        print("Procs created: ", procs_number)
        print("Time: {0:.2f} s".format(time2))

        self.assertTrue(time2 < time1)

if __name__ == '__main__':
    unittest.main()
