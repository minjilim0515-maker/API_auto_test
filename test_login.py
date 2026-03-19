from common.request_util import RequestUtil


def test_login():
    url = 'https://reqres.in/api/login'
    data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    res = RequestUtil.send_request('post',url, json=data)
    assert "token" in res.json()
   
