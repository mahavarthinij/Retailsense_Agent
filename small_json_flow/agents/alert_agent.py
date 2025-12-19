import smtplib
from email.message import EmailMessage

class AlertAgent:

    def send(self, product_id, reason, to_email):
        msg = EmailMessage()
        msg["Subject"] = f"Low Stock Alert: {product_id}"
        msg["From"] = "retailshopowner.1988@gmail.com"
        msg["To"] = to_email
        msg.set_content(reason)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("retailshopowner.1988@gmail.com", "tfix mkmv hrql etdr")
            smtp.send_message(msg)

        print(f"📧 Email sent for {product_id}")
