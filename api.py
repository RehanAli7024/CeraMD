from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import re
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

class TranscriptInput(BaseModel):
    transcript: list

@app.post("/process-transcript")
async def process_transcript(input_data: TranscriptInput):
    system_prompt = """
    You are a helpful AI that corrects medical transcripts.
    - Identify speakers as either "Doctor" or "Patient."
    - Merge fragmented sentences when necessary.
    - Extract the patient's name if mentioned and Include the patient's name in a separate field called "patient_name" in the JSON response.
    - Ensure correct grammar and punctuation.
    - Return the response in the same JSON format without any additional text.
    """

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Fix the following JSON transcript:\n{json.dumps(input_data.dict(), indent=2)}"}
        ],
        "temperature": 0.2
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if match:
            extracted_json = match.group(0)
            try:
                output_json = json.loads(extracted_json)
                return output_json
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error: Extracted JSON is invalid.")
        else:
            raise HTTPException(status_code=500, detail="Error: No valid JSON found in response.")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"API Error: {response.text}")
    

from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

@app.post("/generate-differential-diagnosis")
async def generate_differential_diagnosis(input_data: dict):
    soap_note = input_data['soap_note']

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

        differential_diagnosis = completion.choices[0].message.content

        return {"differential_diagnosis": differential_diagnosis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating differential diagnosis: {str(e)}")


@app.post("/generate-soap")
async def generate_soap(input_data: dict):
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
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
