from fastapi import FastAPI
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

    profile = await generate_profile(request.url)

    return profile
