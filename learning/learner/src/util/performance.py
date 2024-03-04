import os


def memory_usage():
    """ Return the memory usage in MB """
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / float(1024*1024)
    return mem
