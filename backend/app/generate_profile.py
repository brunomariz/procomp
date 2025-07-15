import httpx

from app.types import CompanyProfile


async def generate_profile(url: str) -> CompanyProfile:

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    website_text = response.text

    print(website_text)

    profile = CompanyProfile(
        url=url,
        company_name="Example Company",
        company_description="This is an example company.",
        tier1_keywords=["example", "company", "business"],
        tier2_keywords=["sample", "test", "demo"],
        emails=["john@email.com"],
        poc="John Doe",
    )
    return profile
