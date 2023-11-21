import os
from schemas.email import EmailData
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(data: EmailData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to,
                subject='Inicio de sesión',
                html_content='<strong>Prueba notificaciones</strong>'
            )

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                print(sg.api_key)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                return "ok"
            except Exception as e:
                return str(e)
        except Exception:
            return "ko"
    else:
        return "ko"
        
