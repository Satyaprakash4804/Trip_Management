from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

def generate_attendance_pdf(filename, attendance_list, title="Attendance Report"):
    """
    attendance_list: list of dicts from SQL
    """
    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated on: {datetime.datetime.now()}")

    y = height - 110

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Name")
    c.drawString(200, y, "Role")
    c.drawString(280, y, "Status")
    c.drawString(350, y, "Landmark")
    c.drawString(450, y, "Time")

    c.line(50, y - 5, 550, y - 5)
    y -= 30

    c.setFont("Helvetica", 10)
    for row in attendance_list:
        if y < 50:
            c.showPage()
            y = height - 100

        c.drawString(50, y, str(row.get("name", "")))
        c.drawString(200, y, str(row.get("role", "")))
        c.drawString(280, y, str(row.get("status", "")))
        c.drawString(350, y, str(row.get("landmark", "")))
        c.drawString(450, y, str(row.get("timestamp", "")))

        y -= 20

    c.save()
    return filename
