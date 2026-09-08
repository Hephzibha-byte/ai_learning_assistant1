from gtts import gTTS
import os
import uuid


# =========================================================
# TEXT TO SPEECH
# =========================================================

def text_to_speech(text, language="en"):

    if not text or not text.strip():
        return None

    try:

        os.makedirs("audio", exist_ok=True)

        filename = f"response_{uuid.uuid4().hex}.mp3"

        file_path = os.path.join(
            "audio",
            filename
        )

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.save(file_path)

        return file_path

    except Exception as error:

        print(
            f"Text-to-speech error: {error}"
        )

        return None