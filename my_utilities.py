from PyPDF2 import PdfReader, PdfWriter
from flask import current_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from io import BytesIO
import uuid
import os


# PDF Watermarking and Uploading

upload_folder = "/home/soikot/Documents/files"

def create_watermark(text, image_path=None):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Diagonal text
    c.setFont("Helvetica-Bold", 80)
    c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.15))
    c.saveState()
    c.translate(300, 400)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()

    # Image watermark
    if image_path:
        c.saveState()
        image = ImageReader(image_path)
        img_width, img_height = image.getSize()

        scale = 0.25

        draw_width = img_width * scale
        draw_height = img_height * scale

        margin = 36
        page_width, page_height = letter
        x = page_width - margin - draw_width
        y = margin

        c.drawImage(
            image,
            x,
            y,
            width=draw_width,
            height=draw_height,
            mask='auto',
            preserveAspectRatio=True,
        )
        c.restoreState()

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def add_watermark_and_save(pdf_file):

    file_id = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(upload_folder, file_id)

    text = "N  S  T  U"
    image_path = os.path.join(current_app.static_folder, "images/nstu_logo.png")
    watermark = create_watermark(text, image_path)
    
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        page.merge_page(watermark.pages[0])
        writer.add_page(page)

    with open(file_path, "wb") as f:
        writer.write(f)

    return file_id



# Mailing

import smtplib
import ssl
from email.message import EmailMessage

OTP_EXPIRY_MINUTES = 5

def send_otp_email(recipient_email: str, otp: str) -> None:
    """Send the generated OTP to the recipient via SMTP."""
    smtp_username = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))

    if not smtp_username or not smtp_password:
        raise RuntimeError("SMTP credentials are not configured. Set SMTP_EMAIL and SMTP_PASSWORD environment variables.")

    message = EmailMessage()
    message['Subject'] = 'UniScholarWorks Email Verification OTP'
    message['From'] = smtp_username
    message['To'] = recipient_email
    message.set_content(
        f"Hello,\n\n"
        f"Use the following One Time Password (OTP) to verify your UniScholarWorks account: {otp}.\n"
        f"This code will expire in {OTP_EXPIRY_MINUTES} minutes.\n\n"
        "If you did not request this code, you can ignore this email.\n\n"
        "Best regards,\nThe UniScholarWorks Team"
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        server.send_message(message)

def send_welcome_email(recipient_email: str, name: str) -> None:
    
    smtp_username = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))

    if not smtp_username or not smtp_password:
        raise RuntimeError("SMTP credentials are not configured. Set SMTP_EMAIL and SMTP_PASSWORD environment variables.")

    message = EmailMessage()
    message['Subject'] = 'Welcome to UniScholarWorks'
    message['From'] = smtp_username
    message['To'] = recipient_email
    message.set_content(
        f"Dear {name},\n\n"
        "Welcome to UniScholarWorks! Your account has been successfully created.\n\n"
        "UniScholarWorks is your platform for sharing and discovering academic works.\n\n"


        "Best regards,\nThe UniScholarWorks Team"
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        server.send_message(message)