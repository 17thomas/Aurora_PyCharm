import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os

import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64

def send_email_alert(to_email: str, subject: str, text: str, file_path: str = None):
    """
    Sends an email alert via Brevo.
    If file_path is provided, attaches the file to the email.
    """

    # Configure API key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

    # Initialize API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # Prepare attachments list
    attachments = []
    if file_path:
        try:
            with open(file_path, "rb") as f:
                encoded_file = base64.b64encode(f.read()).decode("utf-8")
            attachments.append({
                "content": encoded_file,
                "name": os.path.basename(file_path)
            })
        except Exception as e:
            print(f"[ATTACHMENT ERROR] Could not attach {file_path}: {e}")

    # Build email
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "aurora.longyearbyen@gmail.com", "name": "Aurora Monitor"},
        subject=subject,
        text_content=text,
        attachment=attachments if attachments else None
    )

    # Send email
    try:
        api_instance.send_transac_email(email)
        print(f"[EMAIL] Sent alert to {to_email}!")
    except ApiException as e:
        print(f"[EMAIL ERROR] {e}")
