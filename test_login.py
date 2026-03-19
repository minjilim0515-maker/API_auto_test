import requests


def test_login():
    url = 'https://reqres.in/api/login'
    data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    res = requests.post(url, json=data)
    print(res.json())
    assert res.status_code == 200
    assert "token" in res.json()
   
