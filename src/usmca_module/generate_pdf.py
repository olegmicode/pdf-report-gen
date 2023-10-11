from PyPDF2 import PdfWriter, PdfReader
import io
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.lib.colors import white, black, lightslategray
from src.usmca_module.service import data_pos, translate_positon_to_pdf, text_center_draw


def usmca_generate_pdf_from_json(json_file_path, output_pdf_path, model_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 8)

    print(data)

    draw_on_page_one(pdf_canvas, data)

    # all canvas page save.
    pdf_canvas.save()
    packet.seek(0)
    canvas_page_pdf = PdfReader(packet)

    existing_pdf = PdfReader(
        open(model_pdf_path, "rb"))
    output = PdfWriter()
    first_page = existing_pdf.pages[0]
    first_page.merge_page(canvas_page_pdf.pages[0])
    output.add_page(first_page)

    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()


def draw_boundary_on_page(pdf_canvas, data):
    # horizonal lines
    x, y, w, h = translate_positon_to_pdf(0, 0, 100, 0)
    pdf_canvas.line(x, y - h, x+w, y)

    x, y, w, h = translate_positon_to_pdf(0, 100, 100, 0)
    pdf_canvas.line(x, y - h, x+w, y)

    #   vertical lines
    x, y, w, h = translate_positon_to_pdf(0, 0, 0, 100)
    pdf_canvas.line(x, y - h, x+w, y)
    print("[vertical]>>>", x, y, x + w, h)

    x, y, w, h = translate_positon_to_pdf(100, 0, 0, 100)
    pdf_canvas.line(x, y - h, x+w, y)
    # single shipment


def draw_on_page_one(pdf_canvas, data):
    pdf_canvas.setFont("Helvetica", 8)

    # 1. BlanketPeriod

    # DateFrom
    x, y, w, h = translate_positon_to_pdf(
        data_pos['BlanketPeriod']['DateFrom']['x'], data_pos['BlanketPeriod']['DateFrom']['y'])

    text_center_draw(pdf_canvas, x, y,
                     data['BlanketPeriod']['DateFrom'], "Helvetica", 6, align="left")
    # DateTo
    x, y, w, h = translate_positon_to_pdf(
        data_pos['BlanketPeriod']['DateTo']['x'], data_pos['BlanketPeriod']['DateTo']['y'])

    text_center_draw(pdf_canvas, x, y,
                     data['BlanketPeriod']['DateTo'], "Helvetica", 6, align="left")

    # 2.single shipment (SingleShipment)
    single_shipment = data['SingleShipment']
    val = "Yes" if single_shipment else "No"
    x, y, w, h = translate_positon_to_pdf(
        data_pos['SingleShipment']['x'], data_pos['SingleShipment']['y'])

    text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

    # 3. ReferenceNumber
    val = data['ReferenceNumber']
    x, y, w, h = translate_positon_to_pdf(
        data_pos['ReferenceNumber']['x'], data_pos['ReferenceNumber']['y'])

    text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")
    for group_key in ['Certifier', 'Exporter', 'Producer', 'Importer']:
        # 4. Certifier
        group_data = data[group_key]

        # CompanyName
        val = group_data['CompanyName']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['CompanyName']['x'], data_pos[group_key]['CompanyName']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # Address
        val = group_data['Address']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Address']['x'], data_pos[group_key]['Address']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # City
        val = group_data['City'] + "  " + group_data['StateOrProvince']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['City']['x'], data_pos[group_key]['City']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # PostalCode + CountryCode
        val = group_data['PostalCode'] + " , " + group_data['CountryCode']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['PostalCode']['x'], data_pos[group_key]['PostalCode']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # Phone
        val = group_data['Phone']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Phone']['x'], data_pos[group_key]['Phone']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # TaxID
        val = "Tax ID: " + group_data['TaxID']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['TaxID']['x'], data_pos[group_key]['TaxID']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

        # Email
        val = group_data['Email']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Email']['x'], data_pos[group_key]['Email']['y'])

        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

    # 11. I CERTIFY THAT:
    group_value = data['Signatory']
    for v_key in ['Name', 'CompanyName', 'Title', 'Email', 'Phone', 'Date']:
        val = group_value[v_key]
        x, y, w, h = translate_positon_to_pdf(
            data_pos['Signatory'][v_key]['x'], data_pos['Signatory'][v_key]['y'])
        text_center_draw(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

    pdf_canvas.showPage()


def draw_new_page(pdf_canvas, draw_page, data):
    # draw rect
    x1 = draw_page["edge"]["x1"]
    x2 = draw_page["edge"]["x2"]
    y1 = draw_page["edge"]["y1"]
    y2 = draw_page["edge"]["y2"]
    pdf_canvas.line(x1, y1, x2, y1)
    # pdf_canvas.line(x1, y1, x1, y2)
    # pdf_canvas.line(x1, y2, x2, y2)
    # pdf_canvas.line(x2, y2, x2, y1)
    # date

    x = draw_page["date"]["x"]
    y = draw_page["date"]["y"]
    text_center_draw(pdf_canvas, x, y,
                     draw_page["date"]["text"], "Helvetica", 8, ddy)

    text_center_draw(pdf_canvas, draw_page["title"]["x"], draw_page["title"]
                     ["y"], draw_page["title"]["text"], "Helvetica", 14, ddy)
    pdf_canvas.line(draw_page["divider"]["x1"], draw_page["divider"]
                    ["y1"] + ddy, draw_page["divider"]["x2"], draw_page["divider"]["y2"] + ddy)

    text_center_draw(pdf_canvas, 500, 722, "Page", "Helvetica", 13, ddy)
    text_center_draw(pdf_canvas, 380, 700,
                     "Bill of Lading Number:", "Helvetica", 8, ddy)
    x = position_dict["BOL"]["BOLNumber"]["x"]
    y = position_dict["BOL"]["BOLNumber"]["y"] + ddy
    # print(data)
    val = str(data["BOL"]["BOLNumber"])
    text_center_draw(pdf_canvas, 450, 700, val, "Helvetica", 8, ddy)

    pdf_canvas.line(420, 702 + ddy, 560, 702 + ddy)
