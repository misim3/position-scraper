import smtplib
from email.mime.text import MIMEText
from email.header import Header

msg = MIMEText('메일 본문')

msg['Subject'] = Header('메일 제목', 'utf-8')
msg['From'] = 'me@example.com'
msg['To'] = 'you@example.com'

with smtplib.SMTP('localhost') as smtp:
    smtp.send_message(msg)