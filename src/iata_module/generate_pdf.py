from PyPDF2 import PdfWriter, PdfReader
import io
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from barcode.writer import ImageWriter
from reportlab.lib.colors import white, black, lightslategray
from src.iata_module.service import data_pos, first_page_count, page_item_count, translate_positon_to_pdf, text_draw_on_canvas, draw_multiline_string


def iata_generate_pdf_from_json(json_file_path, output_pdf_path, model_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    # draw_boundary_on_page(pdf_canvas, data)

    draw_on_page_one(pdf_canvas, data)

    # draw_new_page(pdf_canvas, data)

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
    # page_count = get_total_page_count(data)
    # for pg_idx in range(1, page_count):
    #     existing_pdf = PdfReader(open(model_pdf_path, "rb"))
    #     next_page = existing_pdf.pages[1]
    #     next_page.merge_page(canvas_page_pdf.pages[pg_idx])
    #     output.add_page(next_page)

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


def draw_on_page_one(pdf_canvas, data):
    # 1. Shipper
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipFrom']['CompanyName']['x'], data_pos['ShipFrom']['CompanyName']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['ShipFrom']['CompanyName'], "Helvetica", 8, align="left")

    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipFrom']['Address']['x'], data_pos['ShipFrom']['Address']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['ShipFrom']['Address'], "Helvetica", 8, align="left")

    val = data['ShipFrom']['City'] + " " + \
        data['ShipFrom']['StateOrProvince'] + \
        " " + data['ShipFrom']['CountryCode']
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipFrom']['City']['x'], data_pos['ShipFrom']['City']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,  val, "Helvetica", 8, align="left")

    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipFrom']['PostalCode']['x'], data_pos['ShipFrom']['PostalCode']['y'])

    text_draw_on_canvas(
        pdf_canvas, x, y, data['ShipFrom']['PostalCode'], "Helvetica", 8, align="left")

    # 2. Air Waybill No
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['AirWaybillNumber']['x'], data_pos['AirWaybillNumber']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['AirWaybillNumber'], "Helvetica", 10, align="left")
    # 3. Shipper's Reference Number
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipperReferenceNumber']['x'], data_pos['ShipperReferenceNumber']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['AirWaybillNumber'], "Helvetica", 10, align="left")
    # 4. Pages
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['Pages']['x'], data_pos['Pages']['y'], data_pos['Pages']['w'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        "1", "Helvetica", 10, align="left")
    text_draw_on_canvas(pdf_canvas, x + _w, y,
                        "1", "Helvetica", 10, align="left")

    # 5. Consignee (ShipTo)
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipTo']['Name']['x'], data_pos['ShipTo']['Name']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['ShipTo']['Name'], "Helvetica", 8, align="left")

    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipTo']['Address']['x'], data_pos['ShipTo']['Address']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,
                        data['ShipTo']['Address'], "Helvetica", 8, align="left")

    val = data['ShipTo']['City'] + " " + \
        data['ShipTo']['StateOrProvince'] + \
        " " + data['ShipTo']['CountryCode']
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipTo']['City']['x'], data_pos['ShipTo']['City']['y'])

    text_draw_on_canvas(pdf_canvas, x, y,  val, "Helvetica", 8, align="left")

    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['ShipTo']['PostalCode']['x'], data_pos['ShipTo']['PostalCode']['y'])

    text_draw_on_canvas(
        pdf_canvas, x, y, data['ShipTo']['PostalCode'], "Helvetica", 8, align="left")
    # company logo
    x, y, w, h = translate_positon_to_pdf(
        data_pos['Logo']['x'], data_pos['Logo']['y'], data_pos['Logo']['w'], data_pos['Logo']['h'])

    image_path = "./src/iata_module/FedEx.jpg"
    pdf_canvas.drawImage(
        image_path, x, y, width=w, height=h)

    # Transport Detail
    # AirService
    val = data['TransportDetails']['AirService']
    x, y, w, h = translate_positon_to_pdf(
        data_pos['TransportDetails']['AirService']['x'], data_pos['TransportDetails']['AirService']['y'], data_pos['TransportDetails']['AirService']['w'], data_pos['TransportDetails']['AirService']['h'])

    if val == "1" or val == "3":
        pdf_canvas.rect(x + w, y, w, h, fill=True)
    elif val == "2":
        pdf_canvas.rect(x, y, w, h, fill=True)
    # AirportOfDeparture
    val = data['TransportDetails']['AirportOfDeparture']
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['TransportDetails']['AirportOfDeparture']['x'], data_pos['TransportDetails']['AirportOfDeparture']['y'])
    text_draw_on_canvas(pdf_canvas, x, y, val, "Helvetica", 8, align="left")
    # AirportOfDestination
    val = data['TransportDetails']['AirportOfDestination']
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['TransportDetails']['AirportOfDestination']['x'], data_pos['TransportDetails']['AirportOfDestination']['y'])
    text_draw_on_canvas(pdf_canvas, x, y, val, "Helvetica", 8, align="left")

    # ShipmentType
    # RadioActive
    val = data['ShipmentType']['RadioActive']
    radio_active_pos = data_pos['ShipmentType']['RadioActive']

    if val:
        x, y, w, h = translate_positon_to_pdf(
            radio_active_pos['active']['x'], radio_active_pos['active']['y'], radio_active_pos['active']['w'], radio_active_pos['active']['h'])
        pdf_canvas.rect(x, y, w, h, fill=True)
    else:
        x, y, w, h = translate_positon_to_pdf(
            radio_active_pos['inactive']['x'], radio_active_pos['inactive']['y'], radio_active_pos['inactive']['w'], radio_active_pos['inactive']['h'])
        pdf_canvas.rect(x, y, w, h, fill=True)

    # Dangerous goods
    dangerous_goods = data['DangerousGoods']
    for good in dangerous_goods:
        x, y, _w, _h = translate_positon_to_pdf(
            data_pos['DangerousGoods']['x'], data_pos['DangerousGoods']['y'])
        line = f"{good['UNNumber']}, {good['PackingType']}, {good['HazmatClass']}, {good['ProperShippingName']}, {good['PackingGroup']} // {good['ActualQuantity']} {good['ActualUOM']} // {good['ActualUOM']}"
        text_draw_on_canvas(pdf_canvas, x, y, line,
                            "Helvetica", 8, align="left")
    # AdditionalHandlingInformation
    additional_handling_information = data['AdditionalHandlingInformation']
    emergency_contact = additional_handling_information['EmergencyContact']
    emergengy_contact_no = additional_handling_information['EmergengyContactNo']
    shipper_name = additional_handling_information['ShipperName']
    shipment_date = additional_handling_information['ShipmentDate']

    val = f"{shipment_date} {shipper_name}    Emergency Contact Tel.No. {emergengy_contact_no}       Emergency Registrant: {emergency_contact}"
    x, y, _w, _h = translate_positon_to_pdf(
        data_pos['AdditionalHandlingInformation']['EmergencyContact']['x'], data_pos['AdditionalHandlingInformation']['EmergencyContact']['y'])
    text_draw_on_canvas(pdf_canvas, x, y, val, "Helvetica", 9, align="left")
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

    # print('[page_count ===>]', page_count)

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
