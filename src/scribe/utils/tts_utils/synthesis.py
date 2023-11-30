from __future__ import annotations

import logging

import torch
from TTS.api import TTS

logger = logging.getLogger(__name__)

#  FROM COQUI TTS
#   def load_tts_model_by_path(
#         self, model_path: str, config_path: str, vocoder_path: str = None, vocoder_config: str = None, gpu: bool = False
#     ):


def synthesise(
    text: str, model: str, language: str = "en", speaker: str = None, output_path: str = None, speaker_wav: str = None
):  # path_mode
    """Synthesise speech from text using a given model.

    Args:
        text (str): Text to synthesise.
        model (str): Path to the model to use for synthesis.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model, device=device)
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
    source_wav: str, target_wav: str, model_name: str = "voice_conversion_models/multilingual/vctk/freevc24", output_path: str = None
):
    """Convert voice from source to target using a given model.

    Args:
        source_wav (str): Path to the source wav file.
        target_wav (str): Path to the target wav file.
        model_name (str): Path to the model to use for voice conversion.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name, device=device)
    if output_path:
        wav = tts.voice_conversion_to_file(source_wav, target_wav, file_path=output_path)
        logger.info(f"Saved voice converted speech to {output_path}.")
    else:
        wav = tts.voice_conversion(source_wav, target_wav)
        return wav


# def tts_vc


def list_models():
    return TTS().list_models()
