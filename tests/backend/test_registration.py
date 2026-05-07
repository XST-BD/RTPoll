import pytest
import random
import requests

BASE_URL = 'http://localhost:8000'


def test_user_registration():

    url = f'{BASE_URL}/api/v0/auth/register'

    # password mismatch =========================================================
    random_num = random.randint(101, 999)
    payload1 = {
        'email': f'tester{random_num}@gmail.com',
        'password': 'pass12345',
        'confirm_password': 'pass54321',
    }
    res = requests.post(url, json=payload1)

    assert res.status_code == 400
    data = res.json()
    assert data['detail'] == "Passwords do not match."


    # short password =========================================================
    random_num = random.randint(101, 999)
    payload2 = {
        'email': f'tester{random_num}@gmail.com',
        'password': 'test123',
        'confirm_password': 'test123',
    }
    res = requests.post(url, json=payload2)

    assert res.status_code == 400
    data = res.json()
    assert data['detail'] == "Password must contain at least 8 characters."


    # invalid mail (nx domain) =========================================================
    payload3 = {
        'email': 'testing@identity.test',
        'password': 'pass12345',
        'confirm_password': 'pass12345',
    }
    res = requests.post(url, json=payload3)

    assert res.status_code == 400
    data = res.json()
    assert data['detail'] == "Please enter a valid email address."


    # invalid mail (regex mismatch) =========================================================
    payload4 = {
        'email': 'testing@identity.test',
        'password': 'pass12345',
        'confirm_password': 'pass12345',
    }
    res = requests.post(url, json=payload4)

    assert res.status_code == 400
    data = res.json()
    assert data['detail'] == "Please enter a valid email address."


    # mail already exists =========================================================
    payload5 = {
        'email': 'tester100@gmail.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }
    res = requests.post(url, json=payload5)

    assert res.status_code == 409
    data = res.json()
    assert data['detail'] == "This email is already registered. Please login."
    

    # all ok =========================================================
    random_num = random.randint(101, 999)
    payload1 = {
        'email': f'tester{random_num}@gmail.com',
        'password': 'pass12345',
        'confirm_password': 'pass12345',
    }
    res = requests.post(url, json=payload1)

    assert res.status_code == 200
    data = res.json()
    assert data['detail'] == "Verification email sent. Please check your inbox."    
    



