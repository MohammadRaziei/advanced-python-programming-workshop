import gradio as gr
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from voice_activity_detection import VoiceActivityDetection, SpeechClass


class WebUI:
    """
    Web-based interface for Voice Activity Detection.
    """

    def __init__(self):
        """
        Initialize the WebUI class.
        """
        self.title = "🎙️ Voice Activity Detection"
        self.description = "Upload an audio file to analyze its speech activity."

    def analyze_audio(self, audio_file):
        """
        Analyze the uploaded audio file for voice activity.

        Parameters:
            audio_file: Path to the uploaded audio file.

        Returns:
            str: Detected speech chunks.
            str: Speech classification.
            np.ndarray: Spectrogram image as a numpy array.
        """
        # Handle case when no audio file is provided
        if not audio_file:
            return "", "", None

        try:
            # Initialize the VoiceActivityDetection class
            vad = VoiceActivityDetection(audio_path=audio_file)

            # Get speech chunks
            chunks = vad.chunks
            formatted_chunks = "\n".join([f"Start: {start:.2f}s, End: {end:.2f}s" for start, end in chunks])

            # Classify the audio
            speech_class = vad.classify().value

            # Generate spectrogram as numpy array
            spectrogram_image = self.generate_spectrogram(audio_file)

            return formatted_chunks, f"Speech Class: {speech_class}", spectrogram_image
        except Exception as e:
            return f"Error: {str(e)}", "", None

    def generate_spectrogram(self, audio_file):
        """
        Generate a spectrogram image from the given audio file.

        Parameters:
            audio_file: Path to the input audio file.

        Returns:
            np.ndarray: Spectrogram image as a numpy array.
        """
        y, sr = librosa.load(audio_file, sr=16000)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_db = librosa.power_to_db(S, ref=np.max)

        # Create a plot for the spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="mel", fmax=8000, cmap="magma")
        plt.colorbar(format="%+2.0f dB")
        plt.title("Mel Spectrogram")
        plt.tight_layout()

        # Convert the figure to a numpy array
        plt.axis("off")  # Remove axis for clean image
        fig = plt.gcf()
        fig.canvas.draw()

        # Convert the figure to a numpy array
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)
        return image

    def launch(self):
        """
        Launch the Gradio web interface.
        """
        with gr.Blocks() as app:
            gr.Markdown(self.title)
            gr.Markdown(self.description)

            with gr.Row():
                audio_input = gr.Audio(label="Upload Audio", type="filepath")
            with gr.Row():
                analyze_button = gr.Button("Analyze")

            with gr.Row():
                with gr.Column():
                    chunks_output = gr.Textbox(label="Detected Speech Chunks", interactive=False)
                    speech_class_output = gr.Textbox(label="Speech Classification", interactive=False)
                with gr.Column():
                    spectrogram_output = gr.Image(label="Spectrogram")

            analyze_button.click(
                self.analyze_audio,
                inputs=[audio_input],
                outputs=[chunks_output, speech_class_output, spectrogram_output]
            )

        app.launch()


# Run the WebUI
if __name__ == "__main__":
    ui = WebUI()
    ui.launch()
