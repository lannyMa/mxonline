#!/usr/bin/env python
# coding=utf-8
import string
from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM


def random_str(randomlength=8):#生成随机字符串用于激活链接后缀
    str = ''
    chars = string.ascii_letters
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):#根据注册类型: 注册or找回密码来判断发哪种邮件
    email_record = EmailVerifyRecord()#每次发邮件记录都记录在EmailVerifyRecord的模型中,用于激活时判断是否有
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register": # 根据send_type定制发送内容
        email_title = "后台在线系统激活链接"
        email_body = "后台在线系统激活链接: http://127.0.0.1:8000/active/{}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email,])
        if send_status:
            pass
    elif send_type == "forget": # forget_pwd.html后发密码重置链接
        email_title = "后台在线密码重置链接"
        email_body = "后台在线系统密码重置链接: http://127.0.0.1:8000/reset_pwd/{}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email,])
        if send_status:
            pass