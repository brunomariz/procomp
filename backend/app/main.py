from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="ProComp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

class CompanyProfile(BaseModel):
    url: str
    company_name: str
    company_description: str
    tier1_keywords: List[str]
    tier2_keywords: List[str]
    emails: List[str]
    poc: str

@app.get("/")
async def root():
    return {"message": "Welcome to the ProComp API!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/analyze-website", response_model=CompanyProfile)
async def analyze_website(request: URLRequest):
    """
    Analyze a website URL and return company information
    """
    # TODO: Add website analysis logic here
    
    return CompanyProfile(
        url=request.url,
        company_name="Example Company",
        company_description="A sample company analysis",
        tier1_keywords=["technology", "innovation"],
        tier2_keywords=["software", "development"],
        emails=["john@example.com"],
        poc="John Doe",
    )

