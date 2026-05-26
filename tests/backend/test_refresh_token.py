import pytest

@pytest.mark.run(order=3)
def test_refresh_token(api_base_url, session):
    
    refresh_url = f"{api_base_url}/api/v0/auth/refresh"
    refresh_res = session.post(refresh_url)
    
    assert refresh_res.status_code == 200


@pytest.mark.run(order=4)
def test_invalid_refresh_token(api_base_url, session):
    
    session.cookies.set("refresh_token", "this-is-not-a-valid-jwt-token")
    response = session.post(f"{api_base_url}/api/v0/auth/refresh")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"


@pytest.mark.run(order=5)
def test_missing_refresh_token(api_base_url, session):
    
    session.cookies.set("refresh_token", "")
    response = session.post(f"{api_base_url}/api/v0/auth/refresh")
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing refresh token"



