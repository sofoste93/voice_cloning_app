import edge_tts
import os
from datetime import datetime


class TextToSpeech:
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice

    async def generate_voice(self, text, output_file=None):
        """
        Convert text to speech and save it as an MP3 file.
        If no output_file is provided, a unique timestamp-based name is generated.
        """
        try:
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                output_file = f"audio/generated_audio_{timestamp}.mp3"

            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            print("🟡 Starting TTS generation...")
            print(f"🎙 Voice: {self.voice}")
            print(f"📄 Text: {text}")

            tts = edge_tts.Communicate(text, self.voice)
            await tts.save(output_file)

            if os.path.exists(output_file):
                print(f"✅ Audio successfully saved: {output_file}")
            else:
                print("❌ Error: Audio file not found after saving.")

            return output_file
        except Exception as e:
            print(f"❌ Error in TTS generation: {e}")
            return None
