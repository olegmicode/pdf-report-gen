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
from src.usmca_module.service import data_pos, first_page_count, page_item_count, translate_positon_to_pdf, text_draw_on_canvas, draw_multiline_string


def usmca_generate_pdf_from_json(json_file_path, output_pdf_path, model_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 8)

    draw_on_page_one(pdf_canvas, data)

    draw_new_page(pdf_canvas, data)

    # all canvas page save.
    pdf_canvas.save()
    packet.seek(0)
    canvas_page_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(model_pdf_path, "rb"))
    output = PdfWriter()
    first_page = existing_pdf.pages[0]
    first_page.merge_page(canvas_page_pdf.pages[0])
    output.add_page(first_page)
    # from page 2nd to ending
    page_count = get_total_page_count(data)
    for pg_idx in range(1, page_count):
        existing_pdf = PdfReader(open(model_pdf_path, "rb"))
        next_page = existing_pdf.pages[1]
        next_page.merge_page(canvas_page_pdf.pages[pg_idx])
        output.add_page(next_page)

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

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['BlanketPeriod']['DateFrom'], "Helvetica", 6, align="left")
    # DateTo
    x, y, w, h = translate_positon_to_pdf(
        data_pos['BlanketPeriod']['DateTo']['x'], data_pos['BlanketPeriod']['DateTo']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['BlanketPeriod']['DateTo'], "Helvetica", 6, align="left")

    # 2.single shipment (SingleShipment)
    single_shipment = data['SingleShipment']
    val = "Yes" if single_shipment else "No"
    x, y, w, h = translate_positon_to_pdf(
        data_pos['SingleShipment']['x'], data_pos['SingleShipment']['y'])

    text_draw_on_canvas(pdf_canvas, x, y, val, "Helvetica", 6, align="left")

    # ReferenceNumber
    val = data['ReferenceNumber']
    x, y, w, h = translate_positon_to_pdf(
        data_pos['ReferenceNumber']['x'], data_pos['ReferenceNumber']['y'])

    text_draw_on_canvas(pdf_canvas, x, y, val, "Helvetica", 6, align="left")
    # CertifyingParty ☑ ☐
    val = data['CertifyingParty']
    check_mark = "\u2713"  # Ballot Box (Unchecked)

    e_x, e_y, e_dx, _ = translate_positon_to_pdf(
        data_pos['CertifyingParty']['exporter']['x'], data_pos['CertifyingParty']['exporter']['y'], data_pos['CertifyingParty']['exporter']['dx'])
    text_draw_on_canvas(pdf_canvas, e_x + e_dx, e_y, 'Exporter',
                        "Helvetica", 8, align="left")

    p_x, p_y, p_dx, _ = translate_positon_to_pdf(
        data_pos['CertifyingParty']['producer']['x'], data_pos['CertifyingParty']['producer']['y'], data_pos['CertifyingParty']['producer']['dx'])
    text_draw_on_canvas(pdf_canvas, p_x + p_dx, p_y, 'Producer',
                        "Helvetica", 8, align="left")
    if val.lower() == 'exporter':
        text_draw_on_canvas(pdf_canvas, e_x, e_y, check_mark,
                            "Helvetica", 8, align="left")
    else:
        text_draw_on_canvas(pdf_canvas, p_x, p_y, check_mark,
                            "Helvetica", 8, align="left")

    # 3 ~ 6. Certifier, Exporter, Producer, Importer
    for group_key in ['Certifier', 'Exporter', 'Producer', 'Importer']:
        # 4. Certifier
        group_data = data[group_key]

        # CompanyName
        val = group_data['CompanyName']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['CompanyName']['x'], data_pos[group_key]['CompanyName']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # Address
        val = group_data['Address']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Address']['x'], data_pos[group_key]['Address']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # City
        val = group_data['City'] + "  " + group_data['StateOrProvince']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['City']['x'], data_pos[group_key]['City']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # PostalCode + CountryCode
        val = group_data['PostalCode'] + " , " + group_data['CountryCode']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['PostalCode']['x'], data_pos[group_key]['PostalCode']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # Phone
        val = group_data['Phone']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Phone']['x'], data_pos[group_key]['Phone']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # TaxID
        val = "Tax ID: " + group_data['TaxID']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['TaxID']['x'], data_pos[group_key]['TaxID']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

        # Email
        val = group_data['Email']
        x, y, w, h = translate_positon_to_pdf(
            data_pos[group_key]['Email']['x'], data_pos[group_key]['Email']['y'])

        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

    # 7 ~ 10 LineItems
    line_items = data['LineItems']
    __x, g_y, __h, g_h = translate_positon_to_pdf(
        data_pos['LineItems']['x'], data_pos['LineItems']['y'], h=data_pos['LineItems']['h'])
    __x, __y, __h, g_dh = translate_positon_to_pdf(
        data_pos['LineItems']['x'], data_pos['LineItems']['y'], h=data_pos['LineItems']['dh'])

    item_y = g_y
    for idx, item in enumerate(line_items):
        if idx < 11:
            for v_key in ['PartNumber', 'Description', 'HSTariffClarification', 'OriginCriterion', 'CountryOfOrigin']:
                x, y, w, h = translate_positon_to_pdf(
                    data_pos['LineItems'][v_key]['x'], data_pos['LineItems'][v_key]['y'], data_pos['LineItems'][v_key]['w'], data_pos['LineItems'][v_key]['h'])
                val = item[v_key]
                align = "left" if v_key in ['Name', 'Description'] else "left"
                if v_key == 'Description':
                    draw_multiline_string(pdf_canvas, val, x,
                                          item_y, w, h)
                else:
                    text_draw_on_canvas(pdf_canvas, x, item_y, val,
                                        "Helvetica", 6, align=align)
            x, y, w, h = translate_positon_to_pdf(0, 0, 100, 0)
            thickness = data_pos['LineItems']['thickness']
            pdf_canvas.setLineWidth(thickness)
            pdf_canvas.line(x, item_y - g_dh, x + w, item_y - g_dh)
            item_y -= g_h

    # 11. I CERTIFY THAT:
    group_value = data['Signatory']
    for v_key in ['Name', 'CompanyName', 'Title', 'Email', 'Phone', 'Date']:
        val = group_value[v_key]
        x, y, w, h = translate_positon_to_pdf(
            data_pos['Signatory'][v_key]['x'], data_pos['Signatory'][v_key]['y'])
        text_draw_on_canvas(pdf_canvas, x, y, val,
                            "Helvetica", 6, align="left")

    pdf_canvas.showPage()


def get_total_page_count(data):
    line_items = data['LineItems']
    line_items_size = len(line_items)

    if line_items_size < first_page_count:
        return 1

    page_count = (line_items_size - first_page_count +
                  page_item_count - 1) // page_item_count + 1
    return page_count


def draw_new_page(pdf_canvas, data):
    line_items = data['LineItems']
    line_items_size = len(line_items)

    page_count = get_total_page_count(data)

    if page_count < 2:
        return

    start_pos = first_page_count

    print('[page_count ===>]', page_count)

    __x, g_y, __h, g_h = translate_positon_to_pdf(
        data_pos['LineItems-2']['x'], data_pos['LineItems-2']['y'], h=data_pos['LineItems-2']['h'])
    __x, __y, __h, g_dh = translate_positon_to_pdf(
        data_pos['LineItems-2']['x'], data_pos['LineItems-2']['y'], h=data_pos['LineItems-2']['dh'])
    for pageIdx in range(1, page_count):
        item_y = g_y
        for idx in range(start_pos, min(start_pos + page_item_count, line_items_size)):
            item = line_items[idx]

            for v_key in ['PartNumber', 'Description', 'HSTariffClarification', 'OriginCriterion', 'CountryOfOrigin']:
                x, y, w, h = translate_positon_to_pdf(
                    data_pos['LineItems-2'][v_key]['x'], data_pos['LineItems-2'][v_key]['y'], data_pos['LineItems-2'][v_key]['w'], data_pos['LineItems-2'][v_key]['h'])
                val = item[v_key]
                align = "left" if v_key in ['Name', 'Description'] else "left"
                if v_key == 'Description':
                    draw_multiline_string(pdf_canvas, val, x,
                                          item_y, w, h)
                else:
                    text_draw_on_canvas(pdf_canvas, x, item_y, val,
                                        "Helvetica", 6, align=align)
            x, y, w, h = translate_positon_to_pdf(0, 0, 100, 0)
            thickness = data_pos['LineItems-2']['thickness']
            pdf_canvas.setLineWidth(thickness)
            pdf_canvas.line(x, item_y - g_dh, x + w, item_y - g_dh)
            item_y -= g_h

        # page action
        pdf_canvas.showPage()
        start_pos = start_pos + page_item_count
