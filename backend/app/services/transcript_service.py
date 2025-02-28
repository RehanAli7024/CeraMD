import requests
import json
import re
from fastapi import HTTPException
from app.config import OPENROUTER_API_KEY, OPENROUTER_API_URL

def process_transcript(input_data):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
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

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if match:
            extracted_json = match.group(0)
            try:
                return json.loads(extracted_json)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error: Extracted JSON is invalid.")
        else:
            raise HTTPException(status_code=500, detail="Error: No valid JSON found in response.")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"API Error: {response.text}")
