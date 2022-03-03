import math
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_parallel(f, a, b, *, executor, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    xs = []
    for i in range(n_iter):
        xs.append(a + i * step)
    ys = executor.map(f.calculate, xs)
    acc += sum(ys) * step
    return acc


class FAtX:
    def __init__(self, f):
        self.f = f

    def calculate(self, x):
        with open("artifacts/medium-logs.txt", "a") as file_medium:
            file_medium.write(f"Calculating {self.f} at {x}. ")
        return self.f(x)


if __name__ == '__main__':
    func = math.cos
    a = 0
    b = math.pi / 2
    n_jobs = 1
    funcClass = FAtX(func)
    cpu_num = multiprocessing.cpu_count()

    times_summary = []
    for n_jobs in range(1, cpu_num * 2):
        start_t = time.process_time()
        executor = ThreadPoolExecutor(max_workers=n_jobs)
        end_t = time.process_time()
        print(integrate_parallel(funcClass, a, b, executor=executor))
        times_summary.append(f"Threadpool with n_jobs={n_jobs} executed in {end_t - start_t}\n")

        start_p = time.process_time()
        executor = ProcessPoolExecutor(max_workers=n_jobs)
        end_p = time.process_time()
        times_summary.append(f"Processpool with n_jobs={n_jobs} executed in {end_p - start_p}\n")
        print(integrate_parallel(funcClass, a, b, executor=executor))

    with open("artifacts/medium-times.txt", "w") as file_medium:
        file_medium.write(f"\n--------\n")
        file_medium.write(f"Time summary:\n")
        file_medium.write("".join(times_summary))
