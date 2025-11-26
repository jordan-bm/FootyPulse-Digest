import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_digest_email(to_email, subject, html_content):
    # Sends HTML digest email using SendGrid

    sg_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FOOTYPULSE_SENDER_EMAIL")

    if not sg_api_key:
        raise ValueError("SENDGRID_API_KEY not found in environment")

    if not from_email:
        raise ValueError("FOOTYPULSE_SENDER_EMAIL not found in environment")

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(sg_api_key)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print("SendGrid Error:", e)
        return None
