import smtplib
from email.mime.text import MIMEText
from llm.decision_engine import decide

# ===== EMAIL CONFIG =====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "retailshopowner.1988@gmail.com"
APP_PASSWORD = "tfix mkmv hrql etdr"
RECEIVER_EMAIL = "supervisorrsa41@gmail.com"


class AlertAgent:

    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("📧 Email sent successfully")

    def handle(self, product_id, stock, reasoning):
        subject = f"🚨 Low Stock Alert: {product_id}"
        body = f"""
           Product: {product_id}
            Stock: {stock}

            Reason:
           {reasoning}
               """
        self.send_email(subject, body)

