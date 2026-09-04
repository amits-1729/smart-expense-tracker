import smtplib
from email.message import EmailMessage

from app.database import settings


def send_reset_email(
    receiver_email: str,
    reset_link: str
):

    message = EmailMessage()

    message["Subject"] = "Reset your Expense Tracker password"
    message["From"] = settings.EMAIL_ADDRESS
    message["To"] = receiver_email

        # Plain-text version
    message.set_content(
        f"""
Hello,

We received a request to reset your Expense Tracker password.

Reset your password using this link:

{reset_link}

This link will expire in 15 minutes.

If you did not request this, you can safely ignore this email.

Regards,
Expense Tracker
"""
    )


    message.add_alternative(
        f"""
        <html>
            <body>
                <h2>Reset your password</h2>

                <p>
                    We received a request to reset your
                    Expense Tracker password.
                </p>

                <p>
                    <a href="{reset_link}">
                        Reset Password
                    </a>
                </p>

                <p>
                    This link will expire in 15 minutes.
                </p>

                <p>
                    If you did not request this,
                    you can safely ignore this email.
                </p>
            </body>
        </html>
        """,
        subtype="html"
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            settings.EMAIL_ADDRESS,
            settings.EMAIL_APP_PASSWORD
        )

        server.send_message(message)
