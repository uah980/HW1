import time
import os
import psutil


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        print("{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before,
            elapsed_time))
        return result

    return wrapper


@profile  # usage of decorator for memory measurement in creating list
def list_create(n):
    print("we have a function that creates and returns some list")
    x = [1] * n
    return x


list_create(20000)


@profile  # usage of decorator for memory and time measurement in creating list with loop
def list_create_2(n):
    print("we have a function that creates and returns some list with loop")
    for i in range(1, 10):
        x = [1, 2, 3] * n
        profile(list.sort)(x)
    return x


l = list_create_2(2000000)
