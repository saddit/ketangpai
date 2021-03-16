import random
import time
from datetime import datetime
import service
import logging
import json
from login import login
import session


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
    semester = config['semester']
    term = config['term']
    username = config['username']
    password = config['password']
    token = config['token']


def init_logging():
    t = datetime.now().strftime("%Y-%m-%d")
    f = open(f'log/{t}.log','w',encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s,%(lineno)d]:%(message)s',
        stream=f
    )


def run():
    courses = service.get_course_list(semester, term)
    for course in courses:
        coursename = course['coursename']
        courseid = course['id']
        logging.info(f'study {coursename}')

        try:
            interact_list = service.get_interact_list(courseid)
        except Exception as e:
            logging.warning(f'{coursename} error:{e}')
            continue

        for interact in interact_list:
            interactid = interact['id']
            interact_title = interact['title']
            try:
                studyStatus: bool = service.check_study_status(interactid)
                # 已经学习完则跳过
                if studyStatus:
                    logging.info(f'[{coursename}]: skip \"{interact_title}\"')
                    continue
                pageCount = service.get_page_count(interactid)
            except Exception:
                logging.warning(f'[{coursename}]:{interact_title} error:{e}')
                continue

            # 遍历ppt记录学习进度
            for i in range(1, pageCount + 1):
                try:
                    msg = service.study_page(interactid, i)
                except Exception as e:
                    logging.warning(
                        f'[{coursename}]:{interact_title} page{i} error:{e}')
                    continue
                logging.info(
                    f'[{coursename},{interact_title}]: page {i} {msg}')
                time.sleep(0.5 + random.uniform(-0.1, 0.2))

            logging.info(f'[{coursename}]: finish {interact_title}')

        logging.info(f'finished {coursename}')

    logging.info('compelete')


if __name__ == '__main__':
    init_logging()
    session.set_token(token)
    try:
        run()
    except:
        logging.info("token已过期，正尝试重新获取")
        token = login(username, password)
        session.set_token(token)
        run()
    if token != config['token']:
        config['token'] = token
        logging.info('正在保存token')
        with open('config.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(config, separators=4))
        logging.info('保存token成功')
