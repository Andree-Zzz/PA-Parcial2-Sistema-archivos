from smtplib import SMTP
from email.message import EmailMessage
import string
from config import settings

message = EmailMessage()

def emailBienvenida(destinatario: string):
    sendEmail(
        'Bienvenido a Clover, Registro Exitoso',
        destinatario,
        '''
        Registro Exitoso.
        Bienvenido a Clover-Flask-PA-P2
        '''
    )

def sendEmail(asunto: string, destinatario: string, mensaje):
    message['Subject'] = asunto
    message['From'] = settings.SMTP_USERNAME
    message['To'] = destinatario
    message.set_content(mensaje)

    username = settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD

    server = SMTP(settings.SMTP_HOSTNAME)
    server.starttls()
    server.login(username,password)
    server.send_message(message)

    server.quit()