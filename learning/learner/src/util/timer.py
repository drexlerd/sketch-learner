import time


class CountDownTimer:
    def __init__(self, seconds):
        self.seconds = seconds
        self.start = time.time()

    def reset(self):
        self.start = time.time()

    def is_expired(self):
        if time.time() - self.start > self.seconds:
            return True
        return False


class Timer:
    def __init__(self, stopped=False):
        self.start_clock_time = time.time()
        self.collected_clock_time = 0
        self.stopped = stopped

    def reset(self):
        self.start_clock_time = time.time()
        self.collected_clock_time = 0

    def resume(self):
        if self.stopped:
            self.start_clock_time = time.time()
            self.stopped = False

    def stop(self):
        if not self.stopped:
            self.collected_clock_time += time.time() - self.start_clock_time
            self.stopped = True

    def get_elapsed_sec(self):
        return self.collected_clock_time

    def get_elapsed_msec(self):
        return self.collected_clock_time * 1000
