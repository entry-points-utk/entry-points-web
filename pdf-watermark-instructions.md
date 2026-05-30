# PDF Watermark & Password Protection

For each event, the raw slides PDF in `public/` needs a watermark and password protection before committing.

## Settings
- Watermark: `DO NOT REPRODUCE` — diagonal (45°), centered, gray, `Helvetica-Bold` size 45
- Password: `entrypoints2026` (owner/edit only — no password required to view)

## Steps

1. Find the commit that first added the raw PDF:
   ```
   git log --oneline -- public/ep-event-X-slides.pdf
   ```

2. Recover the original (pre-watermark) version:
   ```
   git show <hash>:public/ep-event-X-slides.pdf > /tmp/ep-event-X-slides-original.pdf
   ```

3. Create `add_watermark.py` in the project root (update `INPUT` and `OUTPUT` paths):

   ```python
   import io
   from pypdf import PdfReader, PdfWriter
   from reportlab.pdfgen import canvas
   from reportlab.lib.colors import Color

   INPUT  = "/tmp/ep-event-X-slides-original.pdf"
   OUTPUT = "public/ep-event-X-slides.pdf"
   PASSWORD = "entrypoints2026"
   WATERMARK_TEXT = "DO NOT REPRODUCE"

   def make_watermark(width, height):
       packet = io.BytesIO()
       c = canvas.Canvas(packet, pagesize=(width, height))
       c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.3))
       c.setFont("Helvetica-Bold", 45)
       c.translate(width / 2, height / 2)
       c.rotate(45)
       c.drawCentredString(0, 0, WATERMARK_TEXT)
       c.save()
       packet.seek(0)
       return PdfReader(packet).pages[0]

   reader = PdfReader(INPUT)
   if reader.is_encrypted:
       reader.decrypt(PASSWORD)
   writer = PdfWriter()

   for page in reader.pages:
       w = float(page.mediabox.width)
       h = float(page.mediabox.height)
       watermark = make_watermark(w, h)
       page.merge_page(watermark)
       writer.add_page(page)

   writer.encrypt(user_password="", owner_password=PASSWORD)

   with open(OUTPUT, "wb") as f:
       writer.write(f)

   print(f"Done — watermarked and encrypted: {OUTPUT}")
   ```

4. Run it:
   ```
   python3 add_watermark.py
   ```

5. Commit `public/ep-event-X-slides.pdf`, then **delete `add_watermark.py`** before pushing.
