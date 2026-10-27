from fastapi import FastAPI
from app.schemas.petition import PetitionRequest
from fastapi import HTTPException
from app.services.petition_service import analyze_submitted_petition

app = FastAPI(
    title="Academic Petition Triage Service",
    description=(
        "An evidence-based academic petition analysis service. "
        "Final decisions remain with authorized university officers."
    ),
    version="0.2.0",
)


@app.get("/")
def home():
    return {
        "project": "Academic Petition Triage Service",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "petition-api",
    }


@app.post("/petitions/submit")
def submit_petition(petition: PetitionRequest):
    return {
        "message": "Petition received successfully",
        "status": "submitted",
        "petition": petition.model_dump(),
        "triage_status": "pending_analysis",
        "final_decision": "pending_human_review",
    }

@app.post("/petitions/analyze")
def analyze_petition_endpoint(petition: PetitionRequest):
    try:
        result = analyze_submitted_petition(petition.model_dump())
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Petition analysis failed: {exc}",
        ) from exc