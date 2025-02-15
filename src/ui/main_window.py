import os
import asyncio
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from src.tts_engine.tts_model import TextToSpeech
from src.utils.audio_utils import play_audio

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tts_engine = TextToSpeech()

    def initUI(self):
        self.setWindowTitle("Voice Cloning App")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text to convert to voice...")
        layout.addWidget(self.text_input)

        self.generate_button = QPushButton("Generate Voice", self)
        self.generate_button.clicked.connect(self.start_generation)
        layout.addWidget(self.generate_button)

        self.play_button = QPushButton("Play Audio", self)
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)  # Disabled by default
        layout.addWidget(self.play_button)

        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.audio_file = "audio/generated_audio.mp3"

    def start_generation(self):
        """Start the voice generation process in a non-blocking way."""
        loop = asyncio.get_event_loop()
        loop.create_task(self.generate_voice())  # Run asynchronously

    async def generate_voice(self):
        """Generate voice from text and update the UI accordingly."""
        text = self.text_input.toPlainText()
        if not text:
            self.status_label.setText("Error: Please enter some text!")
            return

        self.status_label.setText("Generating voice...")
        result = await self.tts_engine.generate_voice(text, self.audio_file)

        if result and os.path.exists(self.audio_file):
            print(f"✅ Audio file ready: {self.audio_file}")
            self.status_label.setText("Voice generated successfully!")
            self.play_button.setEnabled(True)  # Enable play button
        else:
            self.status_label.setText("❌ Error: Voice generation failed.")

    def play_audio(self):
        """Play the generated audio file."""
        if os.path.exists(self.audio_file):
            play_audio(self.audio_file)
            self.status_label.setText("Playing audio...")
        else:
            print(f"❌ Error: {self.audio_file} not found!")
            self.status_label.setText("Error: No audio file available!")
