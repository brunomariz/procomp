from typing import List

from pydantic import BaseModel


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
