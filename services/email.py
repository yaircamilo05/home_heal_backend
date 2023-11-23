import os
from schemas.email import EmailData, EmailRegisterData
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email_register(data: EmailRegisterData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to
            )
            
            message.dynamic_template_data = {
                'name': data.name,
                'email': to,
                'password': data.password
            }
            
            message.template_id = os.environ.get('TEMPLATE_REGISTER')  

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                response = sg.send(message)
                return "ok"
            except Exception as e:
                return str(e)
        except Exception:
            return "ko"
    else:
        return "ko"
        
def send_email_doctor(data: EmailRegisterData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to
            )
            
            message.dynamic_template_data = {
                'name': data.name,
                'email': to,
                'password': data.password
            }
            
            message.template_id = os.environ.get('TEMPLATE_REGISTER_DOCTOR')  

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                response = sg.send(message)
                return "ok"
            except Exception as e:
                return str(e)
        except Exception:
            return "ko"
    else:
        return "ko"