import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from ... import config

def create_message(from_addr, to_addr, subject, message, encoding):
    body = MIMEText(message, 'plain', encoding)
    body['Subject'] = subject
    body['From'] = from_addr
    body['To'] = to_addr
    body['Date'] = formatdate()
    return body


def send_via_gmail(from_addr, to_addr, body):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login( config['gmail']['user'], config['gmail']['password'])
    s.sendmail(from_addr, [to_addr], body.as_string())
    s.close()


def gmail(message, to_addr):
    body = create_message(
        config['gmail']['user'], to_addr, '[Notification]', message, 'utf8')
    send_via_gmail(config['gmail']['user'], to_addr, body)
    return


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc < 3):
        print('USAGE: python gmail.py address message')
        raise SystemExit(0)
    else:
        to_addr = argvs[1]
        message = argvs[2]

    gmail(message, to_addr)
