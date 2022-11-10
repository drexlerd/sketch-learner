import resource
from . import performance
from . import console

class Clock:
    def __init__(self, name):
        self.name = name
        self.start = None
        self.end = None

    def used_memory(self):
        return performance.memory_usage()

    def elapsed_time(self):
        info_children = resource.getrusage(resource.RUSAGE_CHILDREN)
        info_self = resource.getrusage(resource.RUSAGE_SELF)
        # print("({}) Self: {}".format(os.getpid(), info_self))
        # print("({}) Children: {}".format(os.getpid(), info_children))
        return info_children.ru_utime + info_children.ru_stime + info_self.ru_utime + info_self.ru_stime

    def set_start(self):
        self.start = self.elapsed_time()

    def set_end(self):
        self.end = self.elapsed_time()

    def print(self):
        print("RESOURCES FOR {}: {:.2f} CPU sec - {:.2f} MB".format(self.name, self.end - self.start, self.used_memory()))
