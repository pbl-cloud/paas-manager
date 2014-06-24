import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

argvs = sys.argv
argc = len(argvs)


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
    s.login('pbl.notification@gmail.com', 'uhouhouhouho')
    s.sendmail(from_addr, [to_addr], body.as_string())
    s.close()


def gmail(message, to_addr):
    body = create_message(
        'pbl.notification@gmail.com', to_addr, '[Notification]', message, 'ISO-2022-JP')
    send_via_gmail('pbl.notification@gmail.com', to_addr, body)
    return


if __name__ == '__main__':
    from_addr = 'pbl.notification@gmail.com'
    to_addr = ''

    if (argc < 2):
        message = u'no message.'
    else:
        message = argvs[1]

    body = create_message(
        from_addr, to_addr, '[Notification]', message, 'ISO-2022-JP')

    send_via_gmail(from_addr, to_addr, body)
