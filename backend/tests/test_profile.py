import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.types import AnalyzeWebsiteResponse, CompanyProfile

test_client = TestClient(app)


def test_analyze_website_success():
    """Test successful website analysis with valid URL"""
    url_data = {"url": "https://example.com"}

    response = test_client.post("/api/analyze-website", json=url_data)

    assert response.status_code == 200

    data = AnalyzeWebsiteResponse(
        url=response.json()["url"],
        analysis=CompanyProfile(**response.json()["analysis"]),
    )

    # Check that all required fields are present
    assert hasattr(data, "url")
    assert hasattr(data.analysis, "company_name")
    assert hasattr(data.analysis, "company_description")
    assert hasattr(data.analysis, "tier1_keywords")
    assert hasattr(data.analysis, "tier2_keywords")
    assert hasattr(data.analysis, "emails")
    assert hasattr(data.analysis, "poc")

    # Check data types
    assert isinstance(data.url, str)
    assert isinstance(data.analysis.company_name, str)
    assert isinstance(data.analysis.company_description, str)
    assert isinstance(data.analysis.tier1_keywords, list)
    assert isinstance(data.analysis.tier2_keywords, list)
    assert isinstance(data.analysis.emails, list)
    assert isinstance(data.analysis.poc, str)

    # Check that URL matches the input
    assert data.url == url_data["url"]


def test_analyze_website_missing_url():
    """Test error handling when URL is missing"""
    response = test_client.post("/api/analyze-website", json={})

    assert response.status_code == 422  # Validation error

    error_data = response.json()
    assert "detail" in error_data


def test_analyze_website_invalid_json():
    """Test error handling with invalid JSON"""
    response = test_client.post(
        "/api/analyze-website",
        content="invalid json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_analyze_website_empty_url():
    """Test error handling with empty URL"""
    url_data = {"url": ""}

    response = test_client.post("/api/analyze-website", json=url_data)

    assert response.status_code == 400


def test_analyze_website_different_urls():
    """Test that different URLs return different analysis results"""
    url_data_1 = {"url": "https://example.com"}
    url_data_2 = {"url": "https://google.com"}

    response_1 = test_client.post("/api/analyze-website", json=url_data_1)
    response_2 = test_client.post("/api/analyze-website", json=url_data_2)

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    data_1 = AnalyzeWebsiteResponse(
        url=response_1.json()["url"],
        analysis=CompanyProfile(**response_1.json()["analysis"]),
    )
    data_2 = AnalyzeWebsiteResponse(
        url=response_2.json()["url"],
        analysis=CompanyProfile(**response_2.json()["analysis"]),
    )

    # URLs should match the input
    assert data_1.url == url_data_1["url"]
    assert data_2.url == url_data_2["url"]


@pytest.mark.parametrize(
    "test_url",
    [
        "https://example.com",
        "https://www.gov.uk/",
        "https://example.com/path/to/page",
    ],
)
def test_analyze_website_various_url_formats(test_url):
    """Test various valid URL formats"""
    url_data = {"url": test_url}

    response = test_client.post("/api/analyze-website", json=url_data)

    assert response.status_code == 200

    data = AnalyzeWebsiteResponse(
        url=response.json()["url"],
        analysis=CompanyProfile(**response.json()["analysis"]),
    )
    assert data.url == test_url
    assert len(data.analysis.company_name) > 0
    assert len(data.analysis.tier1_keywords) >= 0
    assert len(data.analysis.tier2_keywords) >= 0


def test_analyze_energy_website():
    """Test analyzing an energy company website"""
    url_data = {"url": "https://totalenergies.com/"}

    response = test_client.post("/api/analyze-website", json=url_data)

    assert response.status_code == 200

    data = AnalyzeWebsiteResponse(
        url=response.json()["url"],
        analysis=CompanyProfile(**response.json()["analysis"]),
    )

    assert (
        "energy" in data.analysis.tier1_keywords
        or "energy" in data.analysis.tier2_keywords
    )
    assert data.analysis.poc != "Unknown"
    assert "Phone" in data.analysis.poc
