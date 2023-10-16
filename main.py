from src.vict_stand_report.generate_pdf import vict_stand_generate_pdf_from_json
from src.commericial_invoice_report.generate_pdf import commericial_invoice_generate_pdf_from_json
from src.usmca_module.generate_pdf import usmca_generate_pdf_from_json
from src.iata_module.generate_pdf import iata_generate_pdf_from_json

# from test import generate_pdf_from_json

vict_stand_generate_pdf_from_json(
    "src/vict_stand_report/data.json", "dist/vict-stand-report.pdf")
commericial_invoice_generate_pdf_from_json(
    "src/commericial_invoice_report/cominv_data.json", 'dist/commericial-invoice-report.pdf')
usmca_generate_pdf_from_json(
    "src/usmca_module/data.json", 'dist/usmca-report.pdf', "src/usmca_module/usmca.pdf")
iata_generate_pdf_from_json(
    "src/iata_module/data.json", 'dist/iata-report.pdf', "src/iata_module/iata.pdf")
