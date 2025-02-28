from openai import OpenAI
from fastapi import HTTPException
from app.config import NVIDIA_API_KEY, NVIDIA_API_URL

client = OpenAI(base_url=NVIDIA_API_URL, api_key=NVIDIA_API_KEY)

def generate_soap(input_data):
    transcript = "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in input_data['transcript']])

    prompt = f"""Generate a detailed SOAP note based on the following doctor-patient conversation:

    {transcript}

    Please structure the SOAP note as follows:
    1. Subjective: Patient's reported symptoms and history
    2. Objective: Any measurable data mentioned (if available)
    3. Assessment: Potential diagnoses based on the information provided
    4. Plan: Recommended tests, treatments, or follow-up actions

    Use only the information provided in the conversation. Do not invent or assume any details not explicitly stated."""

    try:
        completion = client.chat.completions.create(
            model="writer/palmyra-med-70b",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024
        )

        soap_note = completion.choices[0].message.content
        input_data['soap_note'] = soap_note
        return input_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SOAP note: {str(e)}")
