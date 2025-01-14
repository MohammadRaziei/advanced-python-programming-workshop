import webrtcvad
from typing import List, Tuple
from utils import SingletonMeta


class VADModel(metaclass=SingletonMeta):
    """
    Wrapper around WebRTC VAD for processing audio and detecting speech chunks.
    """

    def __init__(self, mode: int = 3, sample_rate: int = 16000, frame_duration: int = 30):
        """
        Initialize the VADModel with WebRTC VAD.

        Parameters:
            mode (int): Aggressiveness mode (0-3). Higher values are more aggressive in filtering out non-speech.
            sample_rate (int): Sample rate of the audio.
            frame_duration (int): Duration of each frame in milliseconds (10, 20, or 30 ms).
        """
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration  # in ms
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(mode)

    def process(self, audio_data: bytes) -> List[Tuple[float, float]]:
        """
        Detect speech chunks from audio data.

        Parameters:
            audio_data (bytes): Raw PCM audio data.

        Returns:
            List[Tuple[float, float]]: List of tuples containing start and end times of speech chunks.
        """
        frame_size = int(self.sample_rate * self.frame_duration / 1000) * 2  # Convert ms to bytes
        chunks = []
        is_speaking = False
        chunk_start = 0
        timestamp = 0

        for i in range(0, len(audio_data), frame_size):
            frame = audio_data[i:i + frame_size]
            if len(frame) < frame_size:
                break

            is_voice = self.vad.is_speech(frame, self.sample_rate)

            if is_voice and not is_speaking:
                is_speaking = True
                chunk_start = timestamp
            elif not is_voice and is_speaking:
                is_speaking = False
                chunks.append((chunk_start, timestamp))

            timestamp += self.frame_duration / 1000

        # Handle end of audio
        if is_speaking:
            chunks.append((chunk_start, timestamp))

        return chunks
