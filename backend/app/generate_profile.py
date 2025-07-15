from app.types import CompanyProfile


async def generate_profile(website_text: str, url: str) -> CompanyProfile:

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
