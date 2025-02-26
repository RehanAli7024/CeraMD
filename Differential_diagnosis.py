from openai import OpenAI
import json

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

# Load the data from the JSON file
with open('output.json', 'r') as f:
    data = json.load(f)

soap_note = data['soap_note']

prompt = f"""Based on the following SOAP note, generate a detailed differential diagnosis:

{soap_note}

Please structure the differential diagnosis as follows:
1. List the most likely diagnoses in order of probability
2. For each diagnosis, provide:
   - Key symptoms or risk factors supporting this diagnosis
   - Recommended tests or procedures to confirm or rule out this diagnosis
3. After listing the diagnoses, provide a "Next Steps" section with recommended actions

Use only the information provided in the SOAP note. Do not invent or assume any details not explicitly stated."""

completion = client.chat.completions.create(
  model="writer/palmyra-med-70b",
  messages=[{"role":"user","content":prompt}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

# Collect the generated differential diagnosis
differential_diagnosis = ""
for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    differential_diagnosis += chunk.choices[0].delta.content

# Update the JSON data with the generated differential diagnosis
data['differential_diagnosis'] = differential_diagnosis

# Write the updated data back to the JSON file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Differential diagnosis has been generated and saved to output.json")
