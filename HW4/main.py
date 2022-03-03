# from timeit import default_timer as timer
import time
from multiprocessing import Process
from threading import Thread


def fib(n):
    seq = [1, 1]
    for i in range(2, n):
        x = seq[i - 2]
        y = seq[i - 1]
        seq.append(x + y)


def fib_thread(n):
    fib_calc = []
    for i in range(10):
        fib_calc.append(Thread(target=fib, args=[n]))
    for t in fib_calc:
        t.start()
    for t in fib_calc:
        t.join()


def fib_process(n):
    fib_calc = []
    for i in range(10):
        fib_calc.append(Process(target=fib, args=(n,)))
    for t in fib_calc:
        t.start()
    for t in fib_calc:
        t.join()


if __name__ == '__main__':
    iters = 30000
    start = time.process_time()
    fib_thread(iters)
    end = time.process_time()
    print(f"Thread: {end - start}")

    start = time.process_time()
    fib_process(iters)
    end = time.process_time()
    print(f"Process: {end - start}")
