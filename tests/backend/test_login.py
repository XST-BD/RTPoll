import pytest

@pytest.mark.run(order=2)
def test_user_login(api_base_url, session, shared_data):
    url = f'{api_base_url}/api/v0/auth/login'

    # wrong mail
    payload1 = {
        'email':'tester9999@gmail.com',
        'password': 'pass12345',
    }
    res = session.post(url, json=payload1)
    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == "Invalid credentials."


    # wrong password
    payload2 = {
        'email': 'tester100@gmail.com',
        'password': 'bruhbruh123',
    }
    res = session.post(url, json=payload2)
    assert res.status_code == 400
    data = res.json()
    assert data['detail'] == "Invalid credentials."


    # unverified user
    payload3 = {
        'email': 'tester1001@gmail.com',
        'password': 'password123',
    }
    res = session.post(url, json=payload3)
    assert res.status_code == 428
    data = res.json()
    assert data['detail'] == "Your email address is not verified yet. Please verify your email before logging in."


    # all ok
    payload4 = {
        'email': 'tester100@gmail.com',
        'password': 'password123',
    }
    res = session.post(url, json=payload4)
    assert res.status_code == 200

    # Extract and save the token
    data = res.json()
    shared_data["access_token"] = data.get("access_token")

