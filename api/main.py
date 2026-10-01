from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.structured import StructuredLLM


app = FastAPI(
    title="LLM Extraction API",
    description="Extract structured data from text using an LLM.",
    version="0.1.0",
)

# Create the extractor once, when the server starts
extractor = StructuredLLM()


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    schema_description: str = Field(..., min_length=1, max_length=2000)


class ExtractResponse(BaseModel):
    success: bool
    data: dict | None = None
    tokens: int = 0
    error: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractResponse)
def extract(request:    ExtractRequest):
    result = extractor.extract(
        user_message=request.text,
        schema_description=request.schema_description,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=502,
            detail=result.get("error", "LLM extraction failed"),
        )

    return ExtractResponse(
        success=True,
        data=result["data"],
        tokens=result.get("tokens", 0),
    )