import requests
import json
from datetime import datetime
import logging

from requests.sessions import session

sess = requests.session()
base_url = 'https://v4.ketangpai.com/'

with open('./config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
    username = config['username']
    password = config['password']


def login(email, password) -> str:
    # get token
    resp = sess.post(
        url=base_url+'/UserApi/login',
        data={
            'email': email,
            'password': password,
            'remember': 0,
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return res['token']
    else:
        info = res['info']
        raise Exception(f'获取token失败,{info}')


def get_tasklist(courseid) -> list:
    resp = sess.get(
        url=base_url+f'PrestudyTaskApi/getTaskLists?courseid={courseid}',
    )
    res = resp.json()
    if res['status'] == 1:
        return res['data']
    else:
        info = res['info']
        raise Exception(f'获取学习任务失败,{info}')


def study_task(interactid):
    res = sess.get(
        url=base_url+f'/PrestudyTaskApi/startStudyTask?interactid={interactid}'
    ).json()
    if res['status'] == 0:
        raise Exception(f'开始task失败,{res["info"]}')
    res = sess.get(
        url=base_url+f'/PrestudyTaskApi/finishStudyTask?interactid={interactid}'
    ).json()
    if res['status'] == 0:
        raise Exception(f'结束task失败,{res["info"]}')
    if not check_task(interactid):
        raise Exception(f'最终检测task失败,{res["info"]}')


def check_task(interactid) ->bool:
    res = sess.get(
        url=base_url+f'/PrestudyTaskApi/isFinishStudyTask?interactid={interactid}'
    ).json()
    return res['state'] == 1


def init_logging():
    f = open(f'log/oktp.log','a',encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s,%(lineno)d]:%(message)s',
        stream=f
    )


if __name__ == '__main__':
    init_logging()
    t = datetime.now().strftime("%Y-%m-%d")
    logging.info(t)
    token = login(username, password)
    tasks = get_tasklist('MDAwMDAwMDAwMLOGpZiIqb9shrVyoQ')
    for task in tasks:
        id = task['fromid']
        title = task['title']
        if check_task(id):
            logging.info(f'skip {title}')
        else:
            try:
                study_task(id)
                logging.info(f'finish {title}')
            except Exception as e:
                logging.warning(f'skip {title} reason {e}')
    

