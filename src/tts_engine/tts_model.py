import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

SOURCE_AUDIO_DIR = Path(__file__).resolve().parents[1] / "audio"
AUDIO_DIR = Path(os.environ.get("NEPTUNE_AUDIO_DIR", SOURCE_AUDIO_DIR))
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


def new_recording_path(suffix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return AUDIO_DIR / f"neptune_{timestamp}_{uuid4().hex[:8]}{suffix}"


class TextToSpeech:
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice
        self._model = None

    async def generate_voice(self, text, output_file=None):
        import edge_tts

        output = Path(output_file) if output_file else new_recording_path(".mp3")
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(f".{uuid4().hex}.part")
        try:
            await edge_tts.Communicate(text, self.voice).save(str(temporary))
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
        return str(output)

    def clone_voice(self, text, references, language):
        """Synthesize locally after the caller has obtained XTTS license acceptance."""
        import soundfile as sf

        for path in references:
            try:
                audio = sf.info(path)
                if audio.frames == 0:
                    raise ValueError("fichier vide")
            except (OSError, RuntimeError, ValueError) as error:
                raise ValueError(f"Référence illisible : {Path(path).name}") from error

        if self._model is None:
            import torch
            from TTS.api import TTS

            device = "cuda" if torch.cuda.is_available() else "cpu"
            previous = os.environ.get("COQUI_TOS_AGREED")
            os.environ["COQUI_TOS_AGREED"] = "1"
            try:
                self._model = TTS(MODEL_NAME).to(device)
            finally:
                if previous is None:
                    os.environ.pop("COQUI_TOS_AGREED", None)
                else:
                    os.environ["COQUI_TOS_AGREED"] = previous

        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        output = new_recording_path(".wav")
        temporary = output.with_name(f".{output.stem}.part.wav")
        try:
            self._model.tts_to_file(
                text=text, speaker_wav=references, language=language, file_path=str(temporary)
            )
            if sf.info(temporary).frames == 0:
                raise RuntimeError("Le modèle a produit un fichier audio vide.")
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
        return str(output)
