import requests

def test_chat_endpoint():
    url = "http://127.0.0.1:5000/chat"
    data = {"query": "I'm feeling shaky and my glucose is 55 mg/dL"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "response" in response.json()