from pydantic import BaseModel
from typing import List

class TranscriptEntry(BaseModel):
    speaker: str
    text: str

class TranscriptInput(BaseModel):
    transcript: List[TranscriptEntry]

class SOAPInput(BaseModel):
    soap_note: str
