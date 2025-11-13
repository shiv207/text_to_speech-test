import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

speech_file_path = "speech.wav" 
model = "playai-tts"
voice = "Fritz-PlayAI"
text = """
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

response_format = "wav"

response = client.audio.speech.create(
    model=model,
    voice=voice,
    input=text,
    response_format=response_format
)

response.write_to_file(speech_file_path)