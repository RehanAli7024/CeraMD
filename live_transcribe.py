import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, Microphone
from queue import Queue
import json
from datetime import datetime

deepgram = DeepgramClient(api_key="05a65a31ba2b797f877bf63d7d5ef8f7eefa60a0")

conversation_history = Queue()  # Thread-safe buffer
current_speaker = "Speaker"  # Implement speaker diarization later

def on_message(self, result, **kwargs):
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) > 0:
        conversation_history.put({
            "speaker": current_speaker,  # Temporary placeholder
            "text": sentence,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{current_speaker}: {sentence}") 

def main():
    try:
        dg_connection = deepgram.listen.live.v("1")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            smart_format=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            diarize=True 
        )

        dg_connection.start(options)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        # Wait until finished
        input("Press Enter to stop recording...\n\n")

        dg_connection.finish()
        microphone.finish()

        # Save conversation history
        save_conversation_history()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

def save_conversation_history():
    # Convert queue to list
    transcript = list(conversation_history.queue)
    
    # Save as JSON
    with open("consultation.json", "w") as f:
        json.dump({
            "transcript": transcript,
            "soap_note": None,  # Placeholder for SOAP note
            "differential_diagnosis": None  # Placeholder for differential diagnosis
        }, f, indent=2)
    
    print("\nConversation history saved to consultation.json")

if __name__ == "__main__":
    main()
