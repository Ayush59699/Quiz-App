import smtplib
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText



SMTP_SERRVER_HOST='localhost'
SMTP_SERVER_PORT=1025
SENDER_ADDRESS='admin@gmail.com'
SENDER_PASSWORD=''


def send_email(to, sub, message):
    msg=MIMEMultipart()
    msg['From']=SENDER_ADDRESS
    msg['To']=to
    msg['Subject']=sub
    msg.attach(MIMEText(message, 'html'))
    
    try:
        with smtplib.SMTP(host=SMTP_SERRVER_HOST, port=SMTP_SERVER_PORT) as s:
            s.login(SENDER_ADDRESS, SENDER_PASSWORD)
            s.send_message(msg)
            s.quit()
        return True
    except Exception as e:
        print(f"Email sending failed:{e}")
        return False
    