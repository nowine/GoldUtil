# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class EmailNotifer(object):
    _DEFAULT_SMTP = 'smtp.163.com'
    _DEFAULT_SENDER = 'nowine@163.com'
    _DEFAULT_AUTH = 'Nil0911'
    _DEFAULT_RECEIVER = '56437515@qq.com'
    def __init__(self, smtp_host=None, sender=None, auth=None, port=465):
        self.host = smtp_host if smtp_host else self._DEFAULT_SMTP
        self.sender = sender if sender else self._DEFAULT_SENDER
        self.auth = auth if auth else self._DEFAULT_AUTH
        self.port = port # SSL Port for SMTP is 465
        self._connect()

    def _connect(self):
        try:
            self.smtp = smtplib.SMTP_SSL()
            self.smtp.connect(self.host, self.port)
            self.smtp.login(self.sender, self.auth)
        except smtplib.SMTPException:
            print('Failed to login {0} on {1}'.format(self.sender, self.host))

    def _build_mail(self, mail_subject, mail_body, from_, to):
        print(mail_body)
        msg = MIMEText(mail_body, 'html')
        msg['Subject'] = Header(mail_subject)
        msg['From'] = Header(from_)
        msg['To'] = Header(to)
        return msg

    def send_mail(self, mail_subject, mail_body, from_=None, to=None):
        from_ = from_ if from_ else self.sender
        to = to if to else self._DEFAULT_RECEIVER
        msg = self._build_mail(mail_subject, mail_body, from_, to)
        print(msg)
        print(msg.as_string())
        try:
            self.smtp.sendmail(from_, to, msg.as_string())
        except smtplib.SMTPException as e:
            print(e)
            print('Failed to send mail to {0}'.format(to))
