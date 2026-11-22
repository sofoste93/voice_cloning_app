import asyncio
import sys

from PyQt6.QtWidgets import QApplication
import qasync

from src import __version__
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Neptune")
    app.setApplicationVersion(__version__)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
