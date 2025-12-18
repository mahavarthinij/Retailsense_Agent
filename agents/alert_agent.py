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

    def handle(self, product, stock):
        print(f"🚧 AlertAgent called for {product}, stock={stock}")

        decision = decide(
            f"Product {product} stock is {stock}. Should we send alert email?"
        )

        print("🤖 LLM decision:", decision)

        if decision and "YES" in decision.upper():
            subject = f"🚨 Low Stock Alert: {product}"
            body = (
                f"Product ID: {product}\n"
                f"Current Stock: {stock}\n\n"
                f"Action Required: Please restock immediately."
            )

            self.send_email(subject, body)
            print(f"🚨 ALERT EMAIL SENT for {product}")
        else:
            print(f"ℹ️ Alert suppressed for {product}")
