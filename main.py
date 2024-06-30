import allFunction
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


if __name__ == '__main__':

    studentid = 'SZ20345999'  # 修改为你自己的学号
    studentpw = '1LX6xSMn^LKeQ*'  # 修改为你的统一登陆密码
    login_params = (studentid, studentpw)


    encrypt_key = b'xtcappscret00330'   # 发送请求时用于加密的字符串，不确定会不会更改


    chaojiying_params = ('username123', 'password456', '789123') # 超级鹰平台的用户名、密码、软件id，请自行注册或者自己写验证码识别模块
    

    hid1 = 'XGJe0tE7loVQjVH6AuF'  # 课程的id，可通过course_get.py等各种方式获取
    hid2 = 'a96lLn4fHWPnpJ06RcV'

    scheduler = BackgroundScheduler()

    scheduler.add_job(allFunction.task_reserve, 'date', run_date='2024-06-30 21:33:00', args=[hid1,encrypt_key,login_params,chaojiying_params]) # 添加选课任务
    scheduler.add_job(allFunction.task_reserve, 'date', run_date='2024-04-29 14:00:00', args=[hid2,encrypt_key,login_params,chaojiying_params])
    
    # 获取课程列表
    # scheduler.add_job(allFunction.course_get, 'date', run_date=datetime.datetime.now(), args=[encrypt_key,login_params])


    scheduler.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping...")
        scheduler.shutdown()




