from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.generate_profile import generate_profile
from app.types import CompanyProfile, URLRequest

app = FastAPI(title="ProComp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    parsed_url = urlparse(request.url)
    if not (parsed_url.scheme in ["http", "https"] and parsed_url.netloc):
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    async with httpx.AsyncClient() as client:
        response = await client.get(request.url)
    website_text = response.text

    profile = await generate_profile(website_text, request.url)

    return profile
