from multiprocessing import Event


class BackgroundProcessManager:
    def __init__(self, max_processes=1):
        self.max_processes = max_processes
        self.processes = {}

    def add_process(self, process, process_id, stop_event: Event = Event()):
        if process_id in self.processes:
            raise ValueError("Process ID already exists.")
        if len(self.processes) >= self.max_processes:
            raise ValueError("Maximum number of processes reached.")
        self.processes[process_id] = {"process": process, "stop_event": stop_event}

    def remove_process(self, process_id):
        self.processes.pop(process_id)

    def get_process(self, process_id):
        return self.processes.get(process_id, None)

    def get_all_processes(self):
        return self.processes

    def stop_process(self, process_id):
        process = self.get_process(process_id)
        if process:
            process["stop_event"].set()
            process["process"].terminate()
            self.remove_process(process_id)
            return True
        return False

    def stop_all_processes(self):
        for process_id in self.processes:
            self.stop_process(process_id)

    def join_process(self, process_id):
        process = self.get_process(process_id)
        if process:
            process["process"].join()
            self.remove_process(process_id)
            return True
        return False

    def join_all_processes(self):
        for process_id in self.processes:
            self.join_process(process_id)
