import pytest
import requests
from io import BytesIO
import numpy as np
import soundfile as sf

from vad_example.voice_activity_detection import VoiceActivityDetection


@pytest.fixture
def sample_audio():
    """
    Fixture to download and provide a sample audio file as BytesIO.

    Returns:
        BytesIO: Audio file content in memory.
    """
    audio_url = "https://models.silero.ai/vad_models/en.wav"
    response = requests.get(audio_url, headers={'User-agent': 'testing 0.1'})
    response.raise_for_status()  # Ensure the request was successful
    return BytesIO(response.content)


@pytest.fixture
def empty_audio():
    """
    Fixture to create an empty audio file as BytesIO.

    Returns:
        BytesIO: Empty audio file content in memory.
    """
    sample_rate = 16000
    audio = np.zeros(0, dtype=np.float32)  # Empty audio
    buffer = BytesIO()
    sf.write(buffer, audio, samplerate=sample_rate, format="WAV")
    buffer.seek(0)
    return buffer


def test_chunks_detection(sample_audio):
    """
    Test to ensure chunks are detected correctly from the sample audio file.
    """
    vad = VoiceActivityDetection(sample_audio)
    chunks = vad.chunks

    assert isinstance(chunks, list), "Chunks should be a list"
    assert all(isinstance(chunk, tuple) and len(chunk) == 2 for chunk in chunks), \
        "Each chunk should be a tuple with start and end times"
    assert all(chunk[0] < chunk[1] for chunk in chunks), \
        "Start time should be less than end time in each chunk"


def test_has_speech(sample_audio):
    """
    Test to ensure speech is detected in the sample audio file.
    """
    vad = VoiceActivityDetection(sample_audio)
    assert vad.has_speech is True, "Speech should be detected in the sample audio"


def test_no_chunks_for_empty_audio(empty_audio):
    """
    Test to ensure no chunks are detected for an empty audio file.
    """
    vad = VoiceActivityDetection(empty_audio)
    assert vad.chunks == [], "No chunks should be detected for an empty audio file"
    assert vad.has_speech is False, "Speech should not be detected in an empty audio file"
