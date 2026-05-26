from datetime import datetime, timedelta
import pytest


@pytest.mark.run(order=6)
def test_create_poll(api_base_url, session, shared_data):
    
    url = f'{api_base_url}/api/v0/poll'

    token = shared_data.get("access_token")
    assert token is not None, "Access token missing from shared_data!"

    expiry = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "question": "What's the biggest desert in the world?",
        "options": ["Shahara", "Arabian", "Great Australian"],
        "expires_at": expiry,
        "result_public": True,
    }
    res = session.post(url, json=payload, headers=headers)
    data = res.json()

    assert res.status_code == 200
    shared_data['poll_id'] = data['id']
    assert data['message'] == 'Poll created'


@pytest.mark.run(order=7)
def test_get_poll_success(api_base_url, session, shared_data):
    
    poll_id = shared_data['poll_id']
    token = shared_data.get("access_token")
    assert token is not None, "Access token missing from shared_data!"

    headers = {"Authorization": f"Bearer {token}"}
    url = f'{api_base_url}/api/v0/poll/{poll_id}'
    res = session.get(url, headers=headers)

    assert res.status_code == 200
    data = res.json()


@pytest.mark.run(order=8)
def test_get_poll_failure(api_base_url, session, shared_data):

    poll_id = '0'
    token = shared_data.get("access_token")
    assert token is not None, "Access token missing from shared_data!"

    headers = {"Authorization": f"Bearer {token}"}
    url = f'{api_base_url}/api/v0/poll/{poll_id}'
    res = session.get(url, headers=headers)

    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == 'Poll not found'


@pytest.mark.run(order=9)
def test_delete_poll_success(api_base_url, session, shared_data):
    
    poll_id = shared_data['poll_id']
    token = shared_data.get("access_token")
    assert token is not None, "Access token missing from shared_data!"

    headers = {"Authorization": f"Bearer {token}"}
    url = f'{api_base_url}/api/v0/poll/{poll_id}'
    res = session.delete(url, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data['message'] == f"Poll: {poll_id} deleted successfully"


@pytest.mark.run(order=10)
def test_delete_poll_failure(api_base_url, session, shared_data):
    
    poll_id = 0
    token = shared_data.get("access_token")
    assert token is not None, "Access token missing from shared_data!"

    headers = {"Authorization": f"Bearer {token}"}
    url = f'{api_base_url}/api/v0/poll/{poll_id}'
    res = session.delete(url, headers=headers)

    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == 'Poll not found'
    