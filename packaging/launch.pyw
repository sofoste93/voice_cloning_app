import os
from pathlib import Path

os.environ["NEPTUNE_AUDIO_DIR"] = str(Path(os.environ["LOCALAPPDATA"]) / "Neptune" / "audio")

from src.main import main

main()
