from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(report):
    """
    Takes the scorecard dictionary and draws it onto a PDF file.
    Returns the PDF as a byte stream so Streamlit can download it.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # 1. Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "DataSense Quality Report")
    
    # 2. Main Score & Grade
    c.setFont("Helvetica", 14)
    c.drawString(50, 710, f"Final Score: {report['total_score']} / 100")
    c.drawString(50, 685, f"Grade: {report['grade']}")
    c.drawString(50, 660, f"Verdict: {report['verdict']}")
    
    # 3. Dimension Breakdown Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 610, "Dimension Breakdown:")
    
    # 4. Loop through dimensions and print them
    y_position = 580
    c.setFont("Helvetica", 12)
    for dim_name, data in report['dimensions'].items():
        c.drawString(70, y_position, f"- {dim_name}: {data['score']} / 20.0 pts")
        y_position -= 25 # Move down the page for the next line
        
    c.save()
    buffer.seek(0)
    return buffer
    