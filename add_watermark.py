import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

INPUT  = "public/ep-event-2-slides.pdf"
OUTPUT = "public/ep-event-2-slides.pdf"
PASSWORD = "entrypoints2026"
WATERMARK_TEXT = "DO NOT REPRODUCE"

def make_watermark(width, height):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    gray = Color(0.5, 0.5, 0.5, alpha=0.3)
    c.setFillColor(gray)
    c.setFont("Helvetica-Bold", 60)
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, WATERMARK_TEXT)
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

reader = PdfReader(INPUT)
writer = PdfWriter()

for page in reader.pages:
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    watermark = make_watermark(w, h)
    page.merge_page(watermark)
    writer.add_page(page)

writer.encrypt(user_password=PASSWORD, owner_password=PASSWORD)

with open(OUTPUT, "wb") as f:
    writer.write(f)

print(f"Done — watermarked and encrypted: {OUTPUT}")
