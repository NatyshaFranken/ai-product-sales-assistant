import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st


def send_download_email(to_email: str, download_link: str) -> None:
    """
    Sends a simple delivery email with the download link.
    Uses Streamlit secrets:
      EMAIL_ENABLED, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
    """
    email_enabled = bool(st.secrets.get("EMAIL_ENABLED", False))
    if not email_enabled:
        return

    smtp_host = st.secrets["SMTP_HOST"]
    smtp_port = int(st.secrets.get("SMTP_PORT", 587))
    smtp_user = st.secrets["SMTP_USER"]
    smtp_password = st.secrets["SMTP_PASSWORD"]
    email_from = st.secrets.get("EMAIL_FROM", smtp_user)

    subject = "✅ Your AI Prompt Mega Pack (Download)"
    text_body = f"""Thanks for your purchase!

Here is your download link:
{download_link}

If you have any issues accessing the files, reply to this email and we’ll help you quickly.
"""

    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, to_email, msg.as_string())