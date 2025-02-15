import edge_tts
import os
import time

class TextToSpeech:
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice

    async def generate_voice(self, text):
        """Convert text to speech and save it as a uniquely named MP3 file."""
        try:
            # Ensure the directory exists
            os.makedirs("audio", exist_ok=True)

            # Generate a unique filename based on timestamp
            timestamp = int(time.time())
            output_file = f"audio/generated_audio_{timestamp}.mp3"

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
