import librosa
import numpy as np
from enum import Enum
from functools import cached_property
from typing import List, Tuple

from model import VADModel
# from utils import Singleton



class SpeechClass(Enum):
    """
    Enumeration to classify speech levels.
    """
    NO_SPEECH = "No Speech"
    LOW_SPEECH = "Low Speech"
    FULL_SPEECH = "Full Speech"



class VoiceActivityDetection:
    """
    Class to perform voice activity detection using VADModel.
    """

    def __init__(self, audio_path: str, mode: int = 3):
        """
        Initialize the VoiceActivityDetection class.

        Parameters:
            audio_path (str): Path to the input audio file.
            mode (int): Aggressiveness mode (0-3). Higher values are more aggressive in filtering out non-speech.
        """
        self.audio_path = audio_path
        self.sample_rate = 16000
        self.audio_data = self._load_audio()
        self.total_duration = len(self.audio_data) / (2 * self.sample_rate)  # Bytes to seconds
        self.model = VADModel(mode=mode, sample_rate=self.sample_rate)

    def _load_audio(self) -> bytes:
        """
        Load audio file and convert it to 16-bit PCM format.

        Returns:
            bytes: Raw PCM audio data.
        """
        audio, _ = librosa.load(self.audio_path, sr=self.sample_rate, mono=True)
        audio = (audio * 32767).astype(np.int16)  # Scale to 16-bit PCM
        return audio.tobytes()

    @cached_property
    def chunks(self) -> List[Tuple[float, float]]:
        """
        Detect speech chunks in the audio file.

        Returns:
            List[Tuple[float, float]]: List of tuples containing start and end times of speech chunks.
        """
        return self.model.process(self.audio_data)

    @property
    def has_speech(self) -> bool:
        """
        Check if the audio file contains speech.

        Returns:
            bool: True if speech is detected, False otherwise.
        """
        return len(self.chunks) > 0

    def calculate_chunk_durations(self) -> float:
        """
        Calculate the duration of all chunks.

        Returns:
            float: Summation of durations for each chunk in seconds.
        """
        return sum([end - start for start, end in self.chunks])

    def classify(self) -> SpeechClass:
        """
        Classify the speech level based on the ratio of speech duration to total audio duration.

        Returns:
            SpeechClass: Classification of the audio as NO_SPEECH, LOW_SPEECH, or FULL_SPEECH.
        """
        speech_duration = self.calculate_chunk_durations()
        speech_ratio = speech_duration / self.total_duration if self.total_duration > 0 else 0

        if speech_ratio < 0.01:
            return SpeechClass.NO_SPEECH
        elif speech_ratio < 0.6:
            return SpeechClass.LOW_SPEECH
        else:
            return SpeechClass.FULL_SPEECH


