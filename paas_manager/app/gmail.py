# -*- coding: utf-8 -*-
import sys
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

argvs = sys.argv
argc = len(argvs)

def create_message(from_addr, to_addr, subject, message, encoding):
    body = MIMEText(message, 'plain', encoding)
    body['Subject'] = Header(subject, encoding)
    body['From'] = from_addr
    body['To'] = to_addr
    body['Date'] = formatdate()
    return body

def send_via_gmail(from_addr, to_addr, body):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('pbl.notification@gmail.com', 'uhouhouhouho')
    s.sendmail(from_addr, [to_addr], body.as_string())
    s.close()

def gmail(message, to_addr):
    body = create_message('pbl.notification@gmail.com', to_addr, u'[Notification]', message, 'ISO-2022-JP')
    send_via_gmail('pbl.notification@gmail.com', to_addr, body)
    return


if __name__ == '__main__':
    from_addr = 'pbl.notification@gmail.com'

    if (argc < 3):
    	print 'USAGE: python gmail.py address message'
        raise SystemExit(0)
    else:
        to_addr = unicode(argvs[1], 'utf-8')
        message = unicode(argvs[2], 'utf-8')
 
    body = create_message(from_addr, to_addr, u'[Notification]', message, 'ISO-2022-JP')

    send_via_gmail(from_addr, to_addr, body)
