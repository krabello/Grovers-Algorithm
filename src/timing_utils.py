class TimingUtils:
    @staticmethod
    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000
            return result, elapsed_time
        return wrapper
