import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
MAIL_USE_TLS = True
SMTP_USERNAME = 'hiraficproject@gmail.com'
SMTP_PASSWORD = 'pfyt egcw egoa kvee'

def send_email(recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")
