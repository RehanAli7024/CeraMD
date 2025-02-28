from openai import OpenAI
from fastapi import HTTPException
from app.config import NVIDIA_API_KEY, NVIDIA_API_URL

client = OpenAI(base_url=NVIDIA_API_URL, api_key=NVIDIA_API_KEY)

def generate_differential_diagnosis(soap_note):
    prompt = f"""Based on the following SOAP note, generate a detailed differential diagnosis:

    {soap_note}

    Please structure the differential diagnosis as follows:
    1. List the most likely diagnoses in order of probability
    2. For each diagnosis, provide:
       - Key symptoms or risk factors supporting this diagnosis
       - Recommended tests or procedures to confirm or rule out this diagnosis
    3. After listing the diagnoses, provide a "Next Steps" section with recommended actions

    Use only the information provided in the SOAP note. Do not invent or assume any details not explicitly stated."""

    try:
        completion = client.chat.completions.create(
            model="writer/palmyra-med-70b",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024
        )

        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating differential diagnosis: {str(e)}")
