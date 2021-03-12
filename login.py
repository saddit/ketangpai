import session
from session import sess


def login(username: str, password: str) -> str:
    login_form = {
        'code': '',
        'email': username,
        'mobile': '',
        'password': password,
        'remember': '0',
        'type': 'login',
    }
    # 登录并获取token
    resp = sess.post(
        url=session.base_url + '/UserApi/login',
        json=login_form
    )
    res = resp.json()
    if res['status'] == 1:
        return res['data']['token']
    else:
        raise Exception(res['message'])
