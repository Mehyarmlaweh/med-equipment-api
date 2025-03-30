import os
from gtts import gTTS  # Import gTTS
from pathlib import Path

def text_to_speech_gtts(text: str, output_path: str = "audio/output.mp3") -> str:
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        tts.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"gTTS error: {str(e)}")