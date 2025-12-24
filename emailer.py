import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER", "").strip()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()

PRODUCT_NAME = os.getenv("PRODUCT_NAME", "Your Product").strip()
PROMPT_PACK_LINK = os.getenv("PROMPT_PACK_LINK", "").strip()
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", EMAIL_SENDER).strip()


def send_email(to_email: str, subject: str, text_body: str, html_body: str | None = None):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise RuntimeError("Missing EMAIL_SENDER or EMAIL_PASSWORD in .env")

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject

    # Plain-text fallback (important)
    msg.set_content(text_body)

    # Pretty HTML version
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


def send_prompt_pack_delivery(customer_email: str):
    if not PROMPT_PACK_LINK:
        raise RuntimeError("Missing PROMPT_PACK_LINK in .env")

    subject = f"Your download: {PRODUCT_NAME}"

    text_body = f"""Thanks for your purchase!

Product: {PRODUCT_NAME}

Here’s your download link:
{PROMPT_PACK_LINK}

Support: {SUPPORT_EMAIL}
If you have any issues, reply to this email.
"""

    html_body = f"""\
<!doctype html>
<html>
  <body style="margin:0; padding:0; background:#f6f7fb; font-family:Arial, sans-serif;">
    <div style="max-width:600px; margin:0 auto; padding:24px;">
      <div style="background:#ffffff; border-radius:14px; padding:22px; border:1px solid #e9ebf2;">
        <h2 style="margin:0 0 12px; font-size:20px; color:#111827;">
          Thanks for your purchase! 🎉
        </h2>

        <p style="margin:0 0 14px; font-size:14px; color:#374151; line-height:1.5;">
          Your <strong>{PRODUCT_NAME}</strong> is ready.
        </p>

        <div style="margin:18px 0 18px;">
          <a href="{PROMPT_PACK_LINK}"
             style="display:inline-block; background:#635bff; color:#ffffff; text-decoration:none;
                    padding:12px 16px; border-radius:10px; font-weight:bold; font-size:14px;">
            Download your pack
          </a>
        </div>

        <p style="margin:0 0 8px; font-size:13px; color:#6b7280; line-height:1.5;">
          If the button doesn’t work, copy & paste this link:
        </p>
        <p style="margin:0 0 16px; font-size:13px;">
          <a href="{PROMPT_PACK_LINK}" style="color:#2563eb; word-break:break-all;">
            {PROMPT_PACK_LINK}
          </a>
        </p>

        <hr style="border:none; border-top:1px solid #eef0f5; margin:16px 0;">

        <p style="margin:0; font-size:13px; color:#6b7280; line-height:1.5;">
          Need help? Reply to this email or contact us at
          <a href="mailto:{SUPPORT_EMAIL}" style="color:#2563eb;">{SUPPORT_EMAIL}</a>.
        </p>
      </div>

      <p style="text-align:center; margin:14px 0 0; font-size:12px; color:#9ca3af;">
        © {PRODUCT_NAME}
      </p>
    </div>
  </body>
</html>
"""

    send_email(customer_email, subject, text_body, html_body)