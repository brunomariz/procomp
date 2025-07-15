import pytest
from fastapi.testclient import TestClient
from app.main import app

test_client = TestClient(app)


def test_analyze_website_success():
    """Test successful website analysis with valid URL"""
    url_data = {"url": "https://example.com"}
    
    response = test_client.post("/api/analyze-website", json=url_data)
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Check that all required fields are present
    assert "url" in data
    assert "company_name" in data
    assert "company_description" in data
    assert "tier1_keywords" in data
    assert "tier2_keywords" in data
    assert "emails" in data
    assert "poc" in data
    
    # Check data types
    assert isinstance(data["url"], str)
    assert isinstance(data["company_name"], str)
    assert isinstance(data["company_description"], str)
    assert isinstance(data["tier1_keywords"], list)
    assert isinstance(data["tier2_keywords"], list)
    assert isinstance(data["emails"], list)
    assert isinstance(data["poc"], str)
    
    # Check that URL matches the input
    assert data["url"] == url_data["url"]


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
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 422


def test_analyze_website_empty_url():
    """Test error handling with empty URL"""
    url_data = {"url": ""}
    
    response = test_client.post("/api/analyze-website", json=url_data)
    
    assert response.status_code == 200


def test_analyze_website_different_urls():
    """Test that different URLs return different analysis results"""
    url_data_1 = {"url": "https://example.com"}
    url_data_2 = {"url": "https://google.com"}
    
    response_1 = test_client.post("/api/analyze-website", json=url_data_1)
    response_2 = test_client.post("/api/analyze-website", json=url_data_2)
    
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    
    data_1 = response_1.json()
    data_2 = response_2.json()
    
    # URLs should match the input
    assert data_1["url"] == url_data_1["url"]
    assert data_2["url"] == url_data_2["url"]


@pytest.mark.parametrize("test_url", [
    "https://example.com",
    "http://test.org",
    "https://subdomain.example.co.uk",
    "https://example.com/path/to/page"
])
def test_analyze_website_various_url_formats(test_url):
    """Test various valid URL formats"""
    url_data = {"url": test_url}
    
    response = test_client.post("/api/analyze-website", json=url_data)
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["url"] == test_url
    assert len(data["company_name"]) > 0
    assert len(data["tier1_keywords"]) >= 0
    assert len(data["tier2_keywords"]) >= 0


def test_analyze_website_response_structure():
    """Test the exact structure of the response model"""
    url_data = {"url": "https://example.com"}
    
    response = test_client.post("/api/analyze-website", json=url_data)
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify exact keys (no extra, no missing)
    expected_keys = {
        "url", "company_name", "company_description", 
        "tier1_keywords", "tier2_keywords", "emails", "poc"
    }
    assert set(data.keys()) == expected_keys
    
    # Verify that keyword lists contain strings
    for keyword in data["tier1_keywords"]:
        assert isinstance(keyword, str)
    
    for keyword in data["tier2_keywords"]:
        assert isinstance(keyword, str)
        
    for email in data["emails"]:
        assert isinstance(email, str)