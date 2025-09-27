from PyPDF2 import PdfReader, PdfWriter
from flask import current_app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from io import BytesIO
import uuid
import os

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