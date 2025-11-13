# filename: simple_tts_mp3.py
import os
import base64
import wave
from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()

# 1) Set your text here
TEXT = """
        Here’s to the crazy ones. The misfits. The rebels. The troublemakers.
        The round pegs in the square holes. The ones who see things differently.
        They’re not fond of rules. And they have no respect for the status quo.
        You can quote them, disagree with them, glorify or vilify them.
        About the only thing you can’t do is ignore them.
        Because they change things.
        They push the human race forward.
        And while some may see them as the crazy ones, we see genius.
        Because the people who are crazy enough to think they can change the world,
        are the ones who do.
"""

# 2) Output audio filename (will be PCM data, not MP3)
OUT_AUDIO = "output.wav"

# 3) Voice (optional). Examples: "Zephyr", "Kore", "Puck", "Umbriel", "Enceladus"
VOICE_NAME = "Zephyr"

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Export it before running.")

    client = genai.Client(api_key=api_key)

    # Request MP3 by specifying an audio format in speech_config
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=TEXT,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE_NAME
                    )
                )
                # Note: Audio format defaults to PCM, MP3 format not available in current version
            ),
        ),
    )

    part = response.candidates[0].content.parts[0]
    if not hasattr(part, 'inline_data') or not part.inline_data or not part.inline_data.data:
        raise RuntimeError("No audio data returned.")
    
    # The data is already decoded PCM bytes (not base64)
    pcm_bytes = part.inline_data.data
    
    # Save as WAV file with proper header
    with wave.open(OUT_AUDIO, 'wb') as wf:
        wf.setnchannels(1)      # Mono
        wf.setsampwidth(2)      # 16-bit
        wf.setframerate(24000)  # 24kHz (TTS output rate)
        wf.writeframes(pcm_bytes)
    
    print(f"Saved {OUT_AUDIO} ({len(pcm_bytes)} bytes of PCM data)")

if __name__ == "__main__":
    main()
