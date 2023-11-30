# running n threads from m processes using queues
class TTSConcurrencyManager:
    def __init__(self, max_processes=1, max_threads=1):
        self.max_processes = max_processes
        self.max_threads = max_threads
        self.processes = {}
        self.threads = {}
