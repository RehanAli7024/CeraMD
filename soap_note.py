import json
import os
from huggingface_hub import InferenceClient

def read_transcript(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['transcript']

def format_transcript(transcript):
    return "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in transcript])

def generate_soap(transcript, api_key):
    client = InferenceClient(model="google/flan-t5-large", token=api_key)

    prompt = f"""Generate SOAP note from clinical conversation:

{transcript}

Structure:
Subjective: [CC, HPI, ROS]
Objective: [Vitals, Physical Exam] 
Assessment: [DDx]
Plan: [Workup]

Use ONLY information from transcript. No interpretations."""

    response = client.text_generation(prompt, max_new_tokens=250)
    return response

def main(json_file_path, api_key):
    transcript_data = read_transcript(json_file_path)
    transcript_text = format_transcript(transcript_data)
    soap_note = generate_soap(transcript_text, api_key)
    return soap_note

if __name__ == "__main__":
    api_key = "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"
    if not api_key:
        raise ValueError("HF_API_KEY environment variable not set")

    json_file_path = "output.json"
    print(main(json_file_path, api_key))
