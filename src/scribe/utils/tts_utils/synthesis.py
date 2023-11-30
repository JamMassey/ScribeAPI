from __future__ import annotations

import logging

import torch
from TTS.api import TTS

logger = logging.getLogger(__name__)


class InMemoryModeLs:
    def __init__(self):
        self.models = {"base": TTS()}  # Should I update and use this? Seems like wasted memory

    def add_model(self, model_name: str, model_path: str):
        self.models[model_name] = TTS(model_path)

    def remove_model(self, model_name: str):
        del self.models[model_name]

    def list_loaded_models(self):
        return self.models.keys()

    def list_available_models(self):
        return self.models["base"].list_models()


def text_to_speech(
    text: str, model: str | TTS, language: str = "en", speaker: str = None, output_path: str = None, speaker_wav: str = None
):  # path_mode
    """Synthesise speech from text using a given model.

    Args:
        text (str): Text to synthesise.
        model (str): Path to the model to use for synthesis.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if isinstance(model, str):
        tts = TTS(model).to(device)
    else:
        tts = model.to(device)
    if tts.is_multi_speaker():
        if speaker is None:
            logger.warning(f"Speaker must be specified for multi-speaker models. Please choose from: {tts.list_speakers()}")
            raise ValueError(f"Speaker must be specified for multi-speaker models. Please choose from: {tts.list_speakers()}")
    if tts.is_multi_language():
        if language is None:
            logger.warning(f"Language must be specified for multi-language models. Please choose from: {tts.list_languages()}")
            raise ValueError(f"Language must be specified for multi-language models. Please choose from: {tts.list_languages()}")
    if output_path:
        wav = tts.tts_to_file(text, speaker, language, speaker_wav, file_path=output_path)
        logger.info(f"Saved synthesised speech to {output_path}.")
    else:
        wav = tts.tts(text, speaker, language, speaker_wav, progress_bar=False)
        return wav


def voice_conversion(
    source_wav: str, target_wav: str, model: str = "voice_conversion_models/multilingual/vctk/freevc24", output_path: str = None
):
    """Convert voice from source to target using a given model.

    Args:
        source_wav (str): Path to the source wav file.
        target_wav (str): Path to the target wav file.
        model_name (str): Path to the model to use for voice conversion.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if isinstance(model, str):
        tts = TTS(model).to(device)
    else:
        tts = model.to(device)
    if output_path:
        wav = tts.voice_conversion_to_file(source_wav, target_wav, file_path=output_path)
        logger.info(f"Saved voice converted speech to {output_path}.")
    else:
        wav = tts.voice_conversion(source_wav, target_wav)
        return wav


def tts_with_vc(text: str, model: str, speaker_wav: str, language: str = "en", speaker: str = None, output_path: str = None):  # path_mode
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if isinstance(model, str):
        tts = TTS(model).to(device)
    else:
        tts = model.to(device)
    if tts.is_multi_speaker():
        if speaker is None:
            logger.warning(f"Speaker must be specified for multi-speaker models. Please choose from: {tts.list_speakers()}")
            raise ValueError(f"Speaker must be specified for multi-speaker models. Please choose from: {tts.list_speakers()}")
    if tts.is_multi_language():
        if language is None:
            logger.warning(f"Language must be specified for multi-language models. Please choose from: {tts.list_languages()}")
            raise ValueError(f"Language must be specified for multi-language models. Please choose from: {tts.list_languages()}")
    if output_path:
        wav = tts.tts_with_vc_to_file(text, language, speaker_wav, output_path, speaker)
        logger.info(f"Saved synthesised speech to {output_path}.")
    else:
        wav = tts.tts_with_vc(text, language, speaker_wav, speaker)
        return wav


# Comes from TTS.utils.audio.numpy_transforms
# def save_wav(*, wav: np.ndarray, path: str, sample_rate: int = None, pipe_out=None, **kwargs) -> None:
#     """Save float waveform to a file using Scipy.

#     Args:
#         wav (np.ndarray): Waveform with float values in range [-1, 1] to save.
#         path (str): Path to a output file.
#         sr (int, optional): Sampling rate used for saving to the file. Defaults to None.
#         pipe_out (BytesIO, optional): Flag to stdout the generated TTS wav file for shell pipe.
#     """
#     wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))

#     wav_norm = wav_norm.astype(np.int16)
#     if pipe_out:
#         wav_buffer = BytesIO()
#         scipy.io.wavfile.write(wav_buffer, sample_rate, wav_norm)
#         wav_buffer.seek(0)
#         pipe_out.buffer.write(wav_buffer.read())
#     scipy.io.wavfile.write(path, sample_rate, wav_norm)


#  FROM COQUI TTS
#   def load_tts_model_by_path(
#         self, model_path: str, config_path: str, vocoder_path: str = None, vocoder_config: str = None, gpu: bool = False
#     ):


def list_models():
    return TTS().list_models()
