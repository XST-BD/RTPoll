import pytest

@pytest.mark.run(order=12)
def test_user_logout(api_base_url, session):
    url = f'{api_base_url}/api/v0/auth/logout'

    res = session.post(url)
    assert res.status_code == 200
    data = res.json()
    assert data['detail'] == "Logged out successfully."
