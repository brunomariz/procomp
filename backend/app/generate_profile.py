import re
from typing import Dict, Optional

from bs4 import BeautifulSoup
from model2vec import StaticModel

from app.types import CompanyProfile
from app.verification import sanitize_html


def extract_company_name(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Check title tag
    title = soup.title.string.strip() if soup.title else None

    # Check meta tags
    meta_title = soup.find("meta", property="og:site_name") or soup.find(
        "meta", property="og:title"
    )
    meta_title_content = (
        meta_title["content"].strip()
        if meta_title and "content" in meta_title.attrs
        else None
    )

    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else None

    # Pick the most likely candidate
    for candidate in [meta_title_content, h1_text, title]:
        if candidate and len(candidate.split()) <= 5:
            return candidate

    return None


def extract_emails(text: str):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)


def guess_poc_simple(html: str) -> Dict[str, Optional[str]]:

    NAME_PATTERN = re.compile(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)+$")  # e.g., John Doe
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE_PATTERN = re.compile(
        r"\+?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}"
    )

    soup = BeautifulSoup(html, "html.parser")
    lines = [
        line.strip()
        for line in soup.get_text(separator="\n").splitlines()
        if line.strip()
    ]

    email, phone, poc = None, None, None

    for i, line in enumerate(lines):
        # --- EMAIL extraction ---
        if not email:
            if "email" in line.lower() and EMAIL_PATTERN.search(line):
                email = line  # prefer full line if labeled
            elif m := EMAIL_PATTERN.search(line):
                email = m.group()

            # Look for name above
            if email:
                for j in range(i - 2, i):
                    if 0 <= j < len(lines) and NAME_PATTERN.match(lines[j]):
                        poc = lines[j]
                        break

        # --- PHONE extraction ---
        if not phone:
            if "phone" in line.lower():
                phone = line  # take full line if labeled
            elif m := PHONE_PATTERN.search(line):
                phone = m.group()

            # Look for name above if not already found
            if phone and not poc:
                for j in range(i - 2, i):
                    if 0 <= j < len(lines) and NAME_PATTERN.match(lines[j]):
                        poc = lines[j]
                        break

        if email and phone and poc:
            break

    return {
        "poc": poc,
        "email": email,
        "phone": phone,
    }


from sklearn.feature_extraction.text import TfidfVectorizer


def generate_keywords_tfidf(text: str, top_n: int = 10):
    """
    Lightweight keyword extractor using TF-IDF (no ML model required).
    Returns top 2 as tier1 and the rest as tier2.
    """
    # Extract candidate keywords as n-grams
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = tfidf_matrix.toarray()[0]
    feature_names = vectorizer.get_feature_names_out()

    # Pair feature names with scores and sort
    scored_keywords = sorted(
        zip(feature_names, scores), key=lambda x: x[1], reverse=True
    )

    # Get top N keyword strings
    keyword_strings = [kw for kw, _ in scored_keywords[:top_n]]
    tier1 = keyword_strings[:2]
    tier2 = keyword_strings[2:]
    return tier1, tier2


async def generate_profile(website_text: str) -> CompanyProfile:

    # Extract company name
    company_name_candidate = extract_company_name(website_text)
    company_name = (
        company_name_candidate if company_name_candidate else "Unknown Company"
    )

    # Extract keywords
    sanitized_text = sanitize_html(website_text)

    # Load a model from the HuggingFace hub (in this case the potion-base-8M model)
    # model = StaticModel.from_pretrained("minishlab/potion-base-8M")

    # from keybert import KeyBERT

    # kw_model = KeyBERT(model=model)
    # keywords = kw_model.extract_keywords(sanitized_text, top_n=10)
    keywords = generate_keywords_tfidf(sanitized_text)

    tier1 = [kw for kw, _ in keywords[:2]]
    tier2 = [kw for kw, _ in keywords[2:]]

    # Extract emails
    emails = extract_emails(sanitized_text)

    # Guess point of contact
    poc_guesses = guess_poc_simple(website_text)
    if poc_guesses["poc"]:
        poc = poc_guesses["poc"]
    elif poc_guesses["email"]:
        poc = poc_guesses["email"]
    elif poc_guesses["phone"]:
        poc = poc_guesses["phone"]
    else:
        poc = None

    profile = CompanyProfile(
        company_name=company_name,
        company_description="This is an example company.",
        tier1_keywords=tier1,
        tier2_keywords=tier2,
        emails=emails,
        poc=poc if poc else "Unknown",
    )

    return profile
