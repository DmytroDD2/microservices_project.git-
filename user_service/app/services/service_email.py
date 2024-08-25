import json
import aiosmtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


load_dotenv()


async def send_email(body):
    try:
        body = json.loads(body)
        message = MIMEText(body['body'], "plain")
        message["From"] = os.getenv("SMTP_USER")
        message["To"] = body['recipient']
        message["Subject"] = body['subject']

        async with aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587) as server:

            await server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            await server.sendmail(os.getenv("SMTP_USER"), [body['recipient']], message.as_string())
            return True

    except (aiosmtplib.SMTPRecipientsRefused, aiosmtplib.SMTPSenderRefused, aiosmtplib.SMTPException) as e:

        return False

    except Exception as e:
        return False


#

