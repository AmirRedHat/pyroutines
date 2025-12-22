import pytest 
from multiprocessing import Queue, Process
import sys
from time import time, sleep
sys.path.append("..")
sys.path.append(".")

from pieroutine.wait_group import WaitGroup
from pieroutine.process import ProcessConcurrent


@pytest.fixture
def numbers():
    return [
        7,5,6,7,2,3,4,4,2,2,5,6,2,1
    ]

def worker_with_wait_group(number, wg):
    res = number * 2
    sleep(number)
    print(f"after sleeping for {number} secs")
    wg.done()
    print(f"number {number} is done")
    return res

def worker_without_wait_group(number):
    res = number * 2
    sleep(number)
    print(f"after sleeping for {number} secs")
    print(f"number {number} is done")
    return res

def test_run_process_with_wait_group__success(numbers):    
    wg = WaitGroup()
    start_time = time()
    pr = ProcessConcurrent(worker_with_wait_group, numbers)
    queue = Queue(maxsize=len(numbers))
    pr.run_process(wg, queue)
    wg.wait()
    queue_result = [queue.get() for _ in range(len(numbers))]
    assert len(queue_result) == len(numbers)
    print("[INFO] Process is done at ", time()-start_time)
    
def test_run_process_originally__success(numbers):
    plist = []
    for num in numbers:
        p = Process(target=worker_without_wait_group, args=(num,))
        p.start()
        plist.append(p)
    count = 0
    for i in plist:
        i.join()
        count += 1
    assert count == len(numbers)