import sys
import asyncio
from PyQt6.QtWidgets import QApplication
import qasync

from src.ui.main_window import MainWindow


def ensure_audio_directory():
    import os
    os.makedirs("audio", exist_ok=True)


def main():
    ensure_audio_directory()
    print("✅ Audio directory ensured.")
    app = QApplication(sys.argv)

    # Create a qasync event loop that integrates with Qt
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    print("🟢 Application started.")

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    print("🚀 Starting Voice Cloning App...")
    main()
