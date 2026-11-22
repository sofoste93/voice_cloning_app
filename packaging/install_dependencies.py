import site
import subprocess
import sys
from pathlib import Path

source = Path(__file__).resolve().parent
target = Path(sys.argv[1]).resolve()
target.mkdir(parents=True, exist_ok=True)
log = target.parent / "installation.log"

# The embedded Python distribution loads pip from the wheel listed in python311._pth.
subprocess.run(
    [
        sys.executable, "-m", "pip", "--disable-pip-version-check", "--log", str(log),
        "install", "--target", str(target), "--upgrade", "--only-binary=:all:",
        "--extra-index-url", "https://download.pytorch.org/whl/cpu",
        "--find-links", str(source), "-r", str(source / "requirements-windows.txt"),
    ],
    check=True,
)
site.addsitedir(str(target))
try:
    from PyQt6.QtMultimedia import QMediaPlayer
    from TTS.tts.models.xtts import Xtts
except Exception:
    import traceback

    with log.open("a", encoding="utf-8") as output:
        traceback.print_exc(file=output)
    raise
