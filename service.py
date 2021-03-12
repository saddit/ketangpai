import session
from session import sess


def get_course_list(semester: str, term: int) -> list:
    # 获取本学期课程列表
    resp = sess.post(
        url=session.base_url + "/CourseApi/semesterCourseList",
        json={
            'isstudy': 1,
            'search': '',
            'semester': semester,
            'term': term
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return res['data']
    else:
        raise Exception(res['message'])


def get_interact_list(courseid: str) -> list:
    # 获得互动课件列表
    resp = sess.post(
        url=session.base_url + '/FutureV2/CourseMeans/getCourseContent',
        json={
            'contenttype': 1,
            'courseid': courseid,
            'coruserole': 0,
            'desc': 3,
            'drid': 0,
            'lessonlink': [],
            'limit': 30,
            'page': 1
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return resp.json()['data']['list']
    else:
        raise Exception(res['message'])
    


def check_study_status(interactid) -> bool:
    # 检查是否已经学习完成
    resp = sess.post(
        url=session.base_url + "/PrestudyTaskApi/getPreStudyInfo",
        json={
            'interactid': interactid
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return resp.json()['data']['studyStatus']
    else:
        raise Exception(res['message'])
    


def get_page_count(interactid) -> int:
    # 获取ppt页码
    resp = sess.post(
        url=session.base_url + '/PrestudyTaskApi/preStudyList',
        json={
            'interactid': interactid
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return resp.json()['data']['pageCount']
    else:
        raise Exception(res['message'])
    


def study_page(interactid, page_index) ->str:
    resp = sess.post(
        url=session.base_url + '/PrestudyTaskApi/studyTaskPageIndex',
        json={
            'interactid': interactid,
            'pageindex': page_index
        }
    )
    res = resp.json()
    if res['status'] == 1:
        return resp.json()['message']
    else:
        raise Exception(res['message'])
    