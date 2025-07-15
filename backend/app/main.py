from urllib.parse import urlparse

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.generate_profile import generate_profile
from app.types import AnalyzeWebsiteResponse, URLRequest
from app.verification import verify_url

app = FastAPI(title="ProComp API", version="1.0.0")


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


@app.post("/api/analyze-website", response_model=AnalyzeWebsiteResponse)
async def analyze_website(request: URLRequest):
    """
    Analyze a website URL and return company information
    """

    verify_url(request.url)

    parsed_url = urlparse(request.url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    page_urls = [request.url]
    for path in ["/about", "/contact", "/contact-form"]:
        candidate_url = f"{base_url}{path}"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(candidate_url, timeout=5)
            if resp.status_code == 200:
                page_urls.append(candidate_url)
        except Exception:
            pass

    website_texts = []
    async with httpx.AsyncClient() as client:
        for url in page_urls:
            try:
                resp = await client.get(url, timeout=10)
                if resp.status_code == 200:
                    website_texts.append(resp.text)
            except Exception:
                continue

    website_text = "\n".join(website_texts)

    profile = await generate_profile(website_text)

    return AnalyzeWebsiteResponse(url=request.url, analysis=profile)
