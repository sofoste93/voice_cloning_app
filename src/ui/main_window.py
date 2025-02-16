import os
import asyncio
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt
from src.tts_engine.tts_model import TextToSpeech
from src.utils.audio_utils import AudioPlayer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_file = None
        self.tts_engine = TextToSpeech()
        self.audio_player = AudioPlayer()  # Persistent audio player with playlist (if available)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Voice Cloning App")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        # Text input area
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text to convert to voice...")
        main_layout.addWidget(self.text_input)

        # Generate voice button
        self.generate_button = QPushButton("Generate Voice", self)
        self.generate_button.clicked.connect(self.start_generation)
        main_layout.addWidget(self.generate_button)

        # Audio control buttons layout
        controls_layout = QHBoxLayout()

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)
        controls_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_audio)
        self.pause_button.setEnabled(False)
        controls_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_audio)
        self.stop_button.setEnabled(False)
        controls_layout.addWidget(self.stop_button)

        self.prev_button = QPushButton("Prev", self)
        self.prev_button.clicked.connect(self.previous_track)
        self.prev_button.setEnabled(False)
        controls_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_track)
        self.next_button.setEnabled(False)
        controls_layout.addWidget(self.next_button)

        main_layout.addLayout(controls_layout)

        # Status label
        self.status_label = QLabel("Status: Ready", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def start_generation(self):
        """Start the voice generation process asynchronously."""
        # Using asyncio.create_task to run the async TTS generation without blocking the UI.
        asyncio.create_task(self.generate_voice())

    async def generate_voice(self):
        """Generate voice from text and update the UI accordingly."""
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("Error: Please enter some text!")
            return

        self.status_label.setText("Generating voice...")
        # Passing None as the filename lets the TTS engine generate a unique name.
        generated_file = await self.tts_engine.generate_voice(text, None)

        if generated_file and os.path.exists(generated_file):
            self.audio_file = generated_file
            self.status_label.setText("Voice generated successfully!")
            print(f"✅ Audio file ready: {self.audio_file}")
            # Update the audio player's playlist (or source) with the new file.
            self.audio_player.clear_playlist()
            self.audio_player.add_audio(self.audio_file)
            # Enable audio control buttons
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.status_label.setText("❌ Error: Voice generation failed.")

    def play_audio(self):
        """Play the generated audio file."""
        if self.audio_file and os.path.exists(self.audio_file):
            self.audio_player.play()
            self.status_label.setText("Playing audio...")
        else:
            self.status_label.setText("Error: No audio file available!")
            print(f"❌ Error: {self.audio_file} not found!")

    def pause_audio(self):
        """Pause the audio playback."""
        self.audio_player.pause()
        self.status_label.setText("Audio paused.")

    def stop_audio(self):
        """Stop the audio playback."""
        self.audio_player.stop()
        self.status_label.setText("Audio stopped.")

    def next_track(self):
        """Play the next track in the playlist."""
        self.audio_player.next()
        self.status_label.setText("Playing next track.")

    def previous_track(self):
        """Play the previous track in the playlist."""
        self.audio_player.previous()
        self.status_label.setText("Playing previous track.")
