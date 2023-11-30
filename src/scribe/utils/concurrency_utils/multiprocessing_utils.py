from multiprocessing import Event

from scribe.utils.tts_utils.synthesis import (
    text_to_speech,
    tts_with_vc,
    voice_conversion,
)

# for running tts in separate processes


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

    def stop_process(self, process_id, remove=True):
        process = self.get_process(process_id)
        if process:
            process["stop_event"].set()
            process["process"].terminate()
            if remove:
                self.remove_process(process_id)
            return True
        return False

    def stop_all_processes(self, remove=True):
        for process_id in self.processes:
            self.stop_process(process_id, remove=remove)

    def join_process(self, process_id, remove=True):
        process = self.get_process(process_id)
        if process:
            process["process"].join()
            if remove:
                self.remove_process(process_id)
            return True
        return False

    def join_all_processes(self, remove=True):
        for process_id in self.processes:
            self.join_process(process_id, remove=remove)


def _text_to_speech(text, model, language, speaker, output_path, speaker_wav, stop_event):
    text_to_speech(text, model, language=language, speaker=speaker, output_path=output_path, speaker_wav=speaker_wav)
    stop_event.set()


def _tts_with_vc(text, model, language, speaker, output_path, speaker_wav, stop_event):
    tts_with_vc(text, model, language=language, speaker=speaker, output_path=output_path, speaker_wav=speaker_wav)
    stop_event.set()


def _voice_conversion(source_wav, target_wav, model, output_path, stop_event):
    voice_conversion(source_wav, target_wav, model, output_path)
    stop_event.set()
