from fpdf import FPDF
import os

def generate_pdf(data, summary, filename="patient_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Patient Intake Summary Report", ln=True, align="C")
    pdf.ln(10)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"\nSummary:\n{summary}")
    save_path = os.path.join("./", filename)
    pdf.output(save_path)
    return save_path