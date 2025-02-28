from fastapi import APIRouter
from app.api.models import TranscriptInput, SOAPInput
from app.services import transcript_service, soap_service, diagnosis_service

router = APIRouter()

@router.post("/process-transcript")
async def process_transcript(input_data: TranscriptInput):
    return transcript_service.process_transcript(input_data)

@router.post("/generate-soap")
async def generate_soap(input_data: TranscriptInput):
    return soap_service.generate_soap(input_data.dict())

@router.post("/generate-differential-diagnosis")
async def generate_differential_diagnosis(input_data: SOAPInput):
    return {"differential_diagnosis": diagnosis_service.generate_differential_diagnosis(input_data.soap_note)}
