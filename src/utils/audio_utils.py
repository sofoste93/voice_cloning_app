import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

# Try to import QMediaPlaylist; if not available, fallback gracefully.
try:
    from PyQt6.QtMultimedia import QMediaPlaylist
except ImportError:
    print("QMediaPlaylist not available in PyQt6.QtMultimedia. Playlist functionality will be limited.")
    QMediaPlaylist = None


class AudioPlayer:
    def __init__(self):
        # Create a persistent QMediaPlayer and set its audio output.
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # Create a playlist if QMediaPlaylist is available.
        if QMediaPlaylist is not None:
            self.playlist = QMediaPlaylist()
            self.player.setPlaylist(self.playlist)
        else:
            self.playlist = None

    def add_audio(self, filepath):
        """Add a new audio file to the playlist or set as source if playlist unsupported."""
        if not os.path.exists(filepath):
            print(f"❌ Error: File {filepath} not found!")
            return
        url = QUrl.fromLocalFile(filepath)
        if self.playlist is not None:
            self.playlist.addMedia(url)
            print(f"🎵 Added audio to playlist: {filepath}")
        else:
            self.player.setSource(url)
            print(f"🎵 Set audio source: {filepath}")

    def clear_playlist(self):
        """Clear all audio tracks from the playlist (if supported)."""
        if self.playlist is not None:
            self.playlist.clear()
            print("🗑️ Playlist cleared.")

    def play(self):
        self.player.play()
        print("▶️ Playback started.")

    def pause(self):
        self.player.pause()
        print("⏸️ Playback paused.")

    def stop(self):
        self.player.stop()
        print("⏹️ Playback stopped.")

    def next(self):
        if self.playlist is not None:
            self.playlist.next()
            print("⏭️ Next track.")
        else:
            print("⏭️ Next track not available (playlist not supported).")

    def previous(self):
        if self.playlist is not None:
            self.playlist.previous()
            print("⏮️ Previous track.")
        else:
            print("⏮️ Previous track not available (playlist not supported).")
