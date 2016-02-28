#!/usr/bin/env python
#-*- coding: utf-8 -*-
 
import email
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
# 邮件列表文件(每行一个邮件地址)
MAIL_FILE_PATH = 'code/e.txt'
 
# 邮件内容文件
MAIL_CONTENT_PATH = 'code/2.txt'
 
# 发件人名称
SENDER_NAME = 'mm'
 
# 发件人邮箱
SENDER_MAIL = 'code/ee.txt'
 
# 发件人邮箱密码
SENDER_PSWD = 'password'
 
# SMTP 服务器
SMTP_SERVER = 'smtp.163.com'
 
# SMTP 端口
SMTP_PORT = '25'
 
# 每次发送给几人
RECEIVER_LIMIT_PER_TIME = 10

# 获取邮箱地址

def GetEmailList():
    f = open(SENDER_MAIL,'r+')

    try:
        lines = f.readlines()
    finally:
        f.close()
    return lines


# 获取收件人列表
def GetReceivers(limit = 10):
    f = open(MAIL_FILE_PATH, 'r+')
 
    try:
        lines = f.readlines()
    finally:
        f.close()
 
    receivers = lines[:RECEIVER_LIMIT_PER_TIME]
    lines     = lines[RECEIVER_LIMIT_PER_TIME:]
 
    f = open(MAIL_FILE_PATH, 'w+')
    f.writelines(lines)
    f.close()
 
    return receivers
 
# 批量发送邮件
def SendEmail(sender, senderName, receivers, subject, body):
    print 1
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.login(SENDER_MAIL, SENDER_PSWD)
 
    if(senderName != ''):
        print senderName
        sender 
 
    for receiver in receivers:
        receiver = receiver.strip()
        print receiver
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        msg.attach(MIMEText(body, 'html', 'utf-8'))
 
        smtp.sendmail(sender, receiver, msg.as_string())
    print 2
    smtp.quit()
 
if __name__ == '__main__':
	'''
	发送邮件开始
	'''
   
	# 获取本次要发送的邮件地址
	receivers = GetReceivers(RECEIVER_LIMIT_PER_TIME)
        print receivers

	# 获取邮件标题和内容
	f = open(MAIL_CONTENT_PATH, 'r');
	lines = f.readlines()
        print 8
        print lines
	f.close()
 
	subject = lines[0].strip()
	body = ''.join(lines[1:])
 
	# 发送
	SendEmail(SENDER_MAIL, SENDER_NAME, receivers, subject, body)
