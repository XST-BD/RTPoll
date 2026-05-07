import pytest
import requests

BASE_URL = 'http://localhost:8000'
session = requests.Session()


def test_user_login():
    url = f'{BASE_URL}/api/v0/auth/login'

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


def test_user_logout():
    url = f'{BASE_URL}/api/v0/auth/logout'

    res = session.post(url)
    assert res.status_code == 200
    data = res.json()
    assert data['detail'] == "Logged out successfully."
