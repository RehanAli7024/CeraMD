from openai import OpenAI
import json

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

# Load the transcript from the JSON file
with open('output.json', 'r') as f:
    data = json.load(f)

transcript = "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in data['transcript']])

prompt = f"""Generate a detailed SOAP note based on the following doctor-patient conversation:

{transcript}

Please structure the SOAP note as follows:
1. Subjective: Patient's reported symptoms and history
2. Objective: Any measurable data mentioned (if available)
3. Assessment: Potential diagnoses based on the information provided
4. Plan: Recommended tests, treatments, or follow-up actions

Use only the information provided in the conversation. Do not invent or assume any details not explicitly stated."""

completion = client.chat.completions.create(
  model="writer/palmyra-med-70b",
  messages=[{"role":"user","content":prompt}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

# Collect the generated SOAP note
soap_note = ""
for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    soap_note += chunk.choices[0].delta.content

# Update the JSON data with the generated SOAP note
data['soap_note'] = soap_note

# Write the updated data back to the JSON file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

print("SOAP note has been generated and saved to output.json")
