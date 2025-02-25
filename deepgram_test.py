from deepgram import Deepgram
import os

# Initialize client with your API key
DEEPGRAM_API_KEY = '05a65a31ba2b797f877bf63d7d5ef8f7eefa60a0'  # Replace with your key
dg_client = Deepgram(DEEPGRAM_API_KEY)

# Transcribe a local audio file
async def transcribe_audio():
    try:
        with open("test_audio.wav", "rb") as audio_file:
            source = {"buffer": audio_file, "mimetype": "audio/wav"}
            response = await dg_client.transcription.prerecorded(source, {"punctuate": True})
            print("Transcript:", response['results']['channels'][0]['alternatives'][0]['transcript'])
    except Exception as e:
        print(f"Error: {e}")

# Run the function
import asyncio
asyncio.run(transcribe_audio())
