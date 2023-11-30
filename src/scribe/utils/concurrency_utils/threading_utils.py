from threading import Event


class ThreadManager:
    def __init__(self, max_threads=None):
        self.max_threads = max_threads
        self.threads = {}

    def add_thread(self, thread, thread_id, stop_event: Event = Event()):
        if thread_id in self.threads:
            raise ValueError("Thread ID already exists.")
        if self.max_threads is not None:
            if len(self.threads) >= self.max_threads:
                raise ValueError("Maximum number of threads reached.")
        self.threads[thread_id] = {"thread": thread, "stop_event": stop_event}

    def remove_thread(self, thread_id):
        self.threads.pop(thread_id)

    def get_thread(self, thread_id):
        return self.threads.get(thread_id, None)

    def get_all_threads(self):
        return self.threads

    def stop_thread(self, thread_id, remove=True):
        thread = self.get_thread(thread_id)
        if thread:
            thread["stop_event"].set()
            thread["thread"].join()
            if remove:
                self.remove_thread(thread_id)
            return True
        return False

    def stop_all_threads(self):
        for thread_id in self.threads:
            self.stop_thread(thread_id)

    def join_thread(self, thread_id, remove=True):
        thread = self.get_thread(thread_id)
        if thread:
            thread["thread"].join()
            if remove:
                self.remove_thread(thread_id)
            return True
        return False

    def join_all_threads(self, remove=True):
        for thread_id in self.threads:
            self.join_thread(thread_id, remove=remove)
