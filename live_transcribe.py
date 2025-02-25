
import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, Microphone



deepgram = DeepgramClient(api_key="05a65a31ba2b797f877bf63d7d5ef8f7eefa60a0")

def main():
    try:
        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcription: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            smart_format=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )

        dg_connection.start(options)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        # Wait until finished
        input("Press Enter to stop recording...\n\n")

        dg_connection.finish()
        microphone.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    main()