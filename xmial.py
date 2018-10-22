# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import os

class Xmail(object):
    def __init__(self):
        self.sender_user = ""
        self.passwd = ""
        self.smtp_server = ""
        self.attaches = []

    def login(self, sender, passwd):
        self.sender = sender
        self.passwd = passwd
        self.set_smtp(sender)
        return self

    def set_smtp(self, sender):
        if '@qq.com' in sender:
            self.smtp_server = 'smtp.qq.com'
        else:
            self.smtp_server = 'smtp.exmail.qq.com'

    def send_mail(self, to, mail):
        try:
            message = MIMEMultipart()
            message['From'] = formataddr([self.sender, self.sender])
            message['To'] = formataddr([to, to])
            message['Subject'] = mail['subject']
            message.attach(MIMEText(mail['content'], 'plain', 'utf-8'))
            for attach in self.attaches:
                message.attach(attach)
            server = self.init_server()
            server.sendmail(self.sender, [to,], message.as_string())
            server.quit()
        except Exception as e:
            print e

    def init_server(self):
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.login(self.sender, self.passwd)
        return server

    def add_attach(self, path):
        attach = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        attach['Content-Type'] = 'application/octet-stream'
        attach['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(path))
        self.attaches.append(attach)
        return self
        
