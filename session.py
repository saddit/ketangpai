import requests

sess = requests.session()

base_url = 'https://openapiv5.ketangpai.com/'

sess.headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Host': 'openapiv5.ketangpai.com',
    'Referer': 'https://www.ketangpai.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'token': 'null',
}

def set_token(token: str):
    sess.headers['token'] = token