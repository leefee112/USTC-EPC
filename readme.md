# EPC课程无人值守选课脚本

## 介绍

本脚本是用于中科大英语口语EPC课程的无人值守自动选课的python脚本。通过此脚本，你无需每天定好闹钟准点登录抢课，但是实测会有3秒左右的延迟，所以不保证一定能抢到课。

本人作为一个非计算机相关专业的学生，代码写得很差，同时在满足需求之后就没有进一步改进，所以进步空间也很大，欢迎各位在此基础上继续修改。

EPC课程的选课需要填写验证码，脚本中使用了[超级鹰](https://www.chaojiying.com)平台用于验证码的识别，需要自行注册或者使用其他验证码平台或者自己写。

最后，由于本人的EPC课程已经选完，本脚本不再进行维护，如有需求请自行修改

## 使用

1. 安装依赖 `pip install -r requirements.txt`
2. 修改`main.py`中的学号、统一登陆密码
3. 获取用于加密的字符串，登录选课界面按F12。找到`Sources`，在`protal/static/js/busi/common-wap.js`中的第57行。（默认值可能也能用，取决于是否发生变化）
4. 注册[超级鹰](https://www.chaojiying.com)平台，填入账号、密码、软件ID，有能力可以自己写验证码识别
5. 修改选课的课程id，设置定时任务，在`main.py`中的19-25行(可以通过`main.py`中第28行course_get获取，也可以通过网页调试获取)

## 手动抢课技巧

本脚本的目的只是实现无人值守选课，实际的选课速度其实比不上手动的理论速度。
手动选课可以在开始选课前的3-4分钟打开选课项目，按F12，定位到验证码、输入框、预约按钮的位置，将此三者的状态由hid改成show，可以提前显示验证码、输入框以及预约按钮。填好验证码卡好时间，准点预约即可。

## 存在的问题

1. 使用了第三方的验证码识别平台，必须连接校外网络，而网络通只能在一台设备中使用，导致实际使用不灵活
2. 实际选课时间会比设定时间延迟3秒，由于代码中每次获取cookie、识别验证码耗时太多

## 参考

1. [中科大EPC课程爬取](https://blog.csdn.net/qq_28491207/article/details/84261732)
2. [Arsennnic/ustc-epc-bot](https://github.com/Arsennnic/ustc-epc-bot/tree/master)
3. [Python爬虫校园网模拟登录](https://zhuanlan.zhihu.com/p/433072666)
4. [超级鹰图像识别Python语言Demo下载](https://www.chaojiying.com/api-14.html)
5. [txtxj/USTC-JWC-Login](https://github.com/txtxj/USTC-JWC-Login)
