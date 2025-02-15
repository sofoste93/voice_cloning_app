import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

def play_audio(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: File {filepath} not found!")
        return

    player = QMediaPlayer()
    player.setSource(QUrl.fromLocalFile(filepath))
    player.play()
    print(f"🎵 Playing audio: {filepath}")
