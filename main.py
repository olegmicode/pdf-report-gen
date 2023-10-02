from src.vict_stand_report.generate_pdf import vict_stand_generate_pdf_from_json
from src.commericial_invoice_report.generate_pdf import commericial_invoice_generate_pdf_from_json

# from test import generate_pdf_from_json

vict_stand_generate_pdf_from_json("src/vict_stand_report/data.json", "dist/vict-stand-report.pdf")
commericial_invoice_generate_pdf_from_json("src/commericial_invoice_report/cominv_data.json", 'dist/commericial-invoice-report.pdf')
