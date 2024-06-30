import datetime
import json
import re
from base64 import b64encode

import pandas as pd
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from chaojiying import Chaojiying_Client


class cookieSession:
    url0 = 'https://passport.ustc.edu.cn/login?service=http://roombooking.cmet.ustc.edu.cn/protal/cas/index'
    url1 = 'https://passport.ustc.edu.cn/login'
    header0 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'connection': 'keep-alive',
        'host': 'passport.ustc.edu.cn',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36'
    }

    header1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'no-cache',
        'content-length': '222',
        'content-type': 'application/x-www-form-urlencoded',
        'host': 'passport.ustc.edu.cn',
        'origin': 'https://passport.ustc.edu.cn',
        'referer': 'https://passport.ustc.edu.cn/login?service=http%3A%2F%2Froombooking.cmet.ustc.edu.cn%2Fprotal%2Fcas%2Findex',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36'
    }

    def __init__(self, username, password):
        self.resp = None
        self.middle_text = None
        self.new_session0 = requests.Session()
        self.new_session1 = requests.Session()
        self.username = username
        self.password = password

    def get_cookie(self):
        self.new_session0.headers.update(self.header0)
        self.resp = self.new_session0.get(self.url0)

        jsessionid = self.new_session0.cookies.get('JSESSIONID')

        # cookies = resp.cookies
        # cookie_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in resp.cookies])

        text = re.search(r'\$\(("#CAS_LT")\)\.val\("([^"]+)"\)', self.resp.text)
        cas_lt = text.group(2)

        data = {
            "model": "uplogin.jsp",
            "CAS_LT": cas_lt,
            "service": "http://roombooking.cmet.ustc.edu.cn/protal/cas/index",
            "warn": "",
            "showCode": "",
            "qrcode": "",
            "resultInput": "",
            "username": self.username,
            "password": self.password
        }

        self.new_session1.cookies.set('JSESSIONID', jsessionid)
        self.new_session1.headers.update(self.header0)
        self.middle_text = self.new_session1.post(self.url0, data=data)

        cookies = self.middle_text.history[1].cookies
        # cookie_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookies])
        jsessionid_cookie = next((cookie for cookie in cookies if cookie.name == 'JSESSIONID'), None)

        # 检查是否找到了名为 'JSESSIONID' 的 cookie
        if jsessionid_cookie:
            # 构造 cookie_string，这里假设只需要值，不需要 name= 的形式
            cookie_string0 = jsessionid_cookie.value
        else:
            # 如果没有找到，可以设置为空字符串或进行其他处理
            cookie_string0 = ''

        return cookie_string0

def task_reserve(hid,encrypt_key,login_params,chaojiying_params):

    studentid, studentpw = login_params
    login_instance = cookieSession(studentid, studentpw)
    cookie_string = login_instance.get_cookie()              # 获取cookie
    capture_img = get_capture_img(cookie_string)  # 获取验证码图片


    username,password,soft_id = chaojiying_params
    chaojiying = Chaojiying_Client(username, password, soft_id)  # 登录验证码识别平台（有能力可以尝试自己识别）
    chaojiying_resp = chaojiying.PostPic(capture_img.content, 1902)  # 验证码识别
    capture_val = chaojiying_resp['pic_str']  # 处理回复获得验证码的值
    print(cookie_string, capture_val)  # 打印一下，总得有个反馈吧


    params_reserve = {'id': hid, 'captcha': capture_val}
    resp_reserve = load_data(urlabs='reserve/doreserve', params=params_reserve, jsessionid=cookie_string, encrypt_key=encrypt_key)  # 提交选课请求
    print(json.loads(resp_reserve.content)['message']) # 返回选课是否成功

def course_get(encrypt_key,login_params):
    studentid, studentpw = login_params
    login_instance = cookieSession(studentid, studentpw)
    cookie_string = login_instance.get_cookie()              # 获取cookie
    course = get_course_list(cookie_string, encrypt_key)             # 获取课程目录
    course.to_excel('course_list.xlsx', index=False)    # 将课程目录写入course_list.xlsx
    print("课程列表写入成功")

def get_course_list(cookie_string0, encrypt_key):
    params_queryCurriculumList = {
        'page': '1',
        'limit': '500',
        'onlyYes': '1',
        'categoryNo': '100005',
        'topicName': '',
        'teachingDayQ': '',
        'teachingDayZ': '',
        'classroomId': '',
        'teacherName': '',
        'seminarMode': '',
        'dayOfWeek': '',
        'teachingWeek': '',
    }
    resp_list = load_data(urlabs='reserve/queryCurriculumList', params=params_queryCurriculumList,
                          jsessionid=cookie_string0, encrypt_key=encrypt_key)
    course_list = json.loads(resp_list.content)['data']['list']
    course_list_form = pd.DataFrame(course_list)
    return course_list_form

def get_capture_img(jsessionid):
    jsession = f'JSESSIONID={jsessionid}'
    jscookie = {'cookie': jsession}
    url0 = 'http://roombooking.cmet.ustc.edu.cn/protal/captcha/captchaImage'
    url = f'{url0}?v={jsession}'
    header0 = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'host': 'roombooking.cmet.ustc.edu.cn',
        'proxy-connection': 'keep-alive',
        'referer': 'http://roombooking.cmet.ustc.edu.cn/protal/home/reserve.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    header1 = header0 | jscookie
    temp_session = requests.session()
    temp_session.cookies.set('JSESSIONID', jsessionid)
    temp_session.headers.update(header1)
    response = temp_session.get(url, headers=header1, verify=False)
    return response

def load_data(urlabs, params, jsessionid, encrypt_key):
    # 拼接完整 URL
    url_root = 'http://roombooking.cmet.ustc.edu.cn/protal'
    url = f"{url_root}/{urlabs}?v={timestamp()}"
    # 加密请求参数
    paramsStr = encrypt(json.dumps(params, separators=(',', ':')), encrypt_key)
    jsession = f'JSESSIONID={jsessionid}'
    jscookie = {'cookie': jsession}

    header0 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'content-length': '64',
        'content-type': 'application/json;charset=UTF-8',
        'host': 'roombooking.cmet.ustc.edu.cn',
        'origin': 'https://roombooking.cmet.ustc.edu.cn',
        'proxy-connection': 'keep-alive',
        'referer': 'http://roombooking.cmet.ustc.edu.cn/protal/home/reserve.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    header1 = header0 | jscookie

    temp_session = requests.session()

    temp_session.cookies.set('JSESSIONID', jsessionid)
    temp_session.headers.update(header1)
    response = temp_session.post(url, data=paramsStr)

    return response

def encrypt(word,encrypt_key):
    key = encrypt_key
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(word.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return b64encode(encrypted_data).decode('utf-8')

def timestamp():
    millisecond = int(datetime.datetime.now().timestamp() * 1000)
    return millisecond
