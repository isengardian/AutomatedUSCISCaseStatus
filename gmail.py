import os, smtplib


class Gmail(object):
    SUBJECT = 'Case Status [Case Number: {0}]'

    def __init__(self):
        passwd = os.environ.get('GMAIL_COMMON_PASSWD')
        self.automate_sender = os.environ.get('GMAIL_AUTOMATE_SENDER')
        self.client = smtplib.SMTP('smtp.gmail.com', 587)
        self.client.ehlo()
        self.client.starttls()
        self.client.login(self.automate_sender, passwd)

    def build_body(self, to, subject, text):
        body = '\r\n'.join([
            'From: %s' % self.automate_sender,
            'To: %s' % to,
            'Subject: %s' % subject,
            '', text, '', "Regards"
        ])
        return body

    def send(self, to, body):
        self.client.sendmail(self.automate_sender, [to], body)

    def close(self):
        self.client.quit()
