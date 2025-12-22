import pytest 
from multiprocessing import Process
import sys
from time import sleep
sys.path.append("..")
sys.path.append(".")

from src.wait_group import RunType, WaitGroup


@pytest.fixture
def numbers():
    return [
        7,5,6,7,2,3,4,4,2,2,5,6,2,1
    ]

def worker(number):
    res = number * 2
    sleep(number)
    print(f"after sleeping for {number} secs")
    print(f"number {number} is done")
    return res


def test__process_wait_for__success():
    number = 2
    process = Process(target=worker, args=(number,))
    try:
        wg = WaitGroup()
        assert wg._process_wait_for(process, number+1)
    finally:
        process.kill()
        print("[TEST] process killed by test function !")
        
def test__process_wait_for__fail():
    number = 4
    process = Process(target=worker, args=(number,))
    try:
        with pytest.raises(TimeoutError):
            wg = WaitGroup()
            wg._process_wait_for(process, number-2)
    finally:
        process.kill()
        print("[TEST] process killed by test function !")

def test_run_with_timeout__success(numbers):
    wg = WaitGroup()
    for num in numbers:
        try:
            wg.wait_for(worker, (num,), 5, RunType.PROCESS)
        except TimeoutError:
            print(f"[TIMEOUT] {num} hit the timeout")