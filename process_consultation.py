import requests
import json
import re

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Load input JSON
with open("consultation.json", "r") as file:
    input_data = json.load(file)

system_prompt = """
You are a helpful AI that corrects medical transcripts.
- Identify speakers as either "Doctor" or "Patient."
- Merge fragmented sentences when necessary.
- Extract the patient’s name if mentioned.
- Ensure correct grammar and punctuation.
- Return the response in the same JSON format without any additional text.
"""

payload = {
    "model": "meta-llama/llama-3-8b-instruct",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Fix the following JSON transcript:\n{json.dumps(input_data, indent=2)}"}
    ],
    "temperature": 0.2
}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    response_text = response.json()["choices"][0]["message"]["content"]

    # Use regex to extract the JSON object
    match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if match:
        extracted_json = match.group(0)

        try:
            output_json = json.loads(extracted_json)
            
            # Save output
            with open("output.json", "w") as file:
                json.dump(output_json, file, indent=2)

            print("✅ Processed transcript saved as output.json")

        except json.JSONDecodeError:
            print("❌ Error: Extracted JSON is invalid.")
    else:
        print("❌ Error: No valid JSON found in response.")

else:
    print(f"❌ API Error: {response.status_code} - {response.text}")
