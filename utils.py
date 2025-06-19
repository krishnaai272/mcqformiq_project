import csv
import smtplib
import qrcode
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

def authenticate(password):
    return password == os.getenv("FORM_PASSWORD", "admin123")

def save_to_csv(data, filename="records.csv"):
    keys = list(data.keys())
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def send_email(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = to_email
    msg.set_content(body)
    with open(attachment_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(attachment_path))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

def generate_qr(link, filename="qr.png"):
    img = qrcode.make(link)
    img.save(filename)
    return filename