import os
from schemas.email import EmailAppointmentData, EmailCancelData, EmailRegisterData, EmailVitalSignsData, EmailLinkData
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
        
def send_email_doctor_admin(data: EmailRegisterData):
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

def send_email_vital_signs(data: EmailVitalSignsData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to,
            )
            
            message.dynamic_template_data = {
                'subject': data.subject,
                'name': data.name,
                'relationship': data.relationship,
                'date': data.date,
                'name_editor': data.name_editor,
                'name_patient': data.name_patient,
                'hearth_rate': data.hearth_rate,
                'state_hearth_rate': data.state_hearth_rate,
                'color_hearth_rate': data.color_hearth_rate,
                'blood_pressure': data.blood_pressure,
                'state_blood_pressure': data.state_blood_pressure,
                'color_blood_pressure': data.color_blood_pressure,
                'o2_saturation': data.o2_saturation,
                'state_o2_saturation': data.state_o2_saturation,
                'color_o2_saturation': data.color_o2_saturation
            }
            
            message.template_id = os.environ.get('TEMPLATE_VITAL_SIGNS')  

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
    
def send_link_email_recory_password(data:EmailLinkData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to,
            )
            
            message.dynamic_template_data = {
                'name': data.name,
                'link': data.link
            }
            
            message.template_id = os.environ.get('TEMPLATE_LINK_RECOVERY_PASSWORD')

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                response = sg.send(message)
                return "ok"
            except Exception as e:
                return "ko"
        except Exception as e:
            return "ko"
    else:
        return "ko"

def send_email_appointment_cancellation(data: EmailCancelData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to,
            )
            
            message.dynamic_template_data = {
                'name': data.name,
                'date': data.date,
            }
            
            message.template_id = os.environ.get('TEMPLATE_APPOINMENT_CANCELLATION')

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                response = sg.send(message)
                return "ok"
            except Exception as e:
                return "ko"
        except Exception as e:
            return "ko"
    else:
        return "ko"

def send_email_appointment_confirmation(data: EmailAppointmentData):
    hash = data.hash
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = data.to_destination
            message = Mail(
                from_email=email_sender,
                to_emails=to,
            )
            
            message.dynamic_template_data = {
                'name': data.name,
                'text': data.text,
                'date': data.date,
                'address': data.address,
                'reason': data.reason,
                'name_patient': data.name_patient,
                'cc_patient': data.cc_patient,
                'phone_patient': data.phone_patient,
                'email_patient': data.email_patient,
                'name_doctor': data.name_doctor,
                'cc_doctor': data.cc_doctor,
                'phone_doctor': data.phone_doctor,
                'email_doctor': data.email_doctor,
                'problem': data.problem,
                'relationship': data.relationship
            }
            
            message.template_id = os.environ.get('TEMPLATE_APPOINMENT_CONFIRMATION')

            try:
                sg = SendGridAPIClient(os.getenv('HOME_HEAL_API_SENDGRID'))
                response = sg.send(message)
                return "ok"
            except Exception as e:
                return "ko"
        except Exception as e:
            return "ko"
    else:
        return "ko"