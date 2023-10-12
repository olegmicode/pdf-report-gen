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
import pandas as pd

# Array
draw_page = {
    "edge": {
        "x1": 40,
        "x2": 570,
        "y1": 720,
        "y2": 20
    },
    "date": {
        "x": 55,
        "y": 722,
        "text": "Date:"
    },
    "page": {
        "x": 55,
        "y": 722,
        "text": "page"
    },
    "title": {
        "x": 300,
        "y": 722,
        "text": "SUPPLEMENT TO THE BILL OF LADING"
    },
    "divider": {
        "x1": 520,
        "y1": 722,
        "x2": 560,
        "y2": 722
    }

}
position_dict = {
    "first_page_number": {
        "x": 540,
        "y": 700
    },
    "next_page_number": {
        "x": 540,
        "y": 720
    },
    "first_page_total": {
        "y": 175
    },

    "shipment_details": {
        "ship_date": {
            "x": 318,
            "y": 686
        },
        "track_no": {
            "x": 321,
            "y": 668
        },
        "invoice_number": {
            "x": 320,
            "y": 650
        },
        "po_number": {
            "x": 454,
            "y": 650
        },
        "payment_terms": {
            "x": 320,
            "y": 632
        },

        "purpose_of_shipment": {
            "x": 315,
            "y": 614
        },
        "origin_state": {
            "x": 318,
            "y": 607
        },
        "country_of_destination": {
            "x": 323,
            "y": 600
        },
        "exporter_phone_no": {
            "x": 315,
            "y": 593
        },
        "incoterms": {
            "x": 323,
            "y": 586
        },
        "bill_of_lading": {
            "x": 454,
            "y": 632
        }

    },

    "exporter": {
        "tax_id": {
            "x": 82,
            "y": 686
        },
        "contact_name": {
            "x": 96,
            "y": 675
        },
        "company_name": {
            "x": 78,
            "y": 638
        },
        "address1": {
            "x": 62,
            "y": 632
        },
        "address2": {
            "x": 51,
            "y": 625
        },
        "city": {
            "x": 50,
            "y": 598
        },
        "state": {
            "x": 70,
            "y": 598
        },
        "postal_code": {
            "x": 90,
            "y": 598
        },
        "country": {
            "x": 95,
            "y": 591
        },
        "phone": {
            "x": 100,
            "y": 665.5
        },
        "email": {
            "x": 84,
            "y": 657
        },
        "parties_to_transaction": {
            "y": 574,
            "related": 52,
            "non_related": 139
        },
    },
    "consignee": {
        "tax_id": {
            "x": 85,
            "y": 551
        },
        "contact_name": {
            "x": 89,
            "y": 540
        },
        "company_name": {
            "x": 76,
            "y": 503
        },
        "address1": {
            "x": 61,
            "y": 496
        },
        "address2": {
            "x": 60,
            "y": 489
        },
        "city": {
            "x": 53,
            "y": 462
        },
        "state": {
            "x": 75,
            "y": 462
        },
        "postal_code": {
            "x": 95,
            "y": 462
        },
        "country": {
            "x": 100,
            "y": 455
        },
        "phone": {
            "x": 101,
            "y": 530
        },
    },



    "sold_to": {

        "same_as_consignee": {
            "x": 305,
            "y": 550
        },
        "tax_id": {
            "x": 345,
            "y": 530
        },
        "contact_name": {
            "x": 306,
            "y": 495
        },
        "company_name": {
            "x": 337,
            "y": 502
        },
        "address1": {
            "x": 319,
            "y": 488
        },
        "address2": {
            "x": 322,
            "y": 481
        },
        "city": {
            "x": 314,
            "y": 462
        },
        "state": {
            "x": 335,
            "y": 462
        },
        "postal_code": {
            "x": 350,
            "y": 462
        },
        "country": {
            "x": 358,
            "y": 454
        },
        "phone": {
            "x": 319,
            "y": 473
        },

    },

    "broker": {

        "name": {
            "x": 110,
            "y": 435
        },
        "phone": {
            "x": 310,
            "y": 435
        },
        "contact_name": {
            "x": 437,
            "y": 435
        },
        "duties_taxes_payable_by": {
            "exporter": {
                "x": 133,
                "y": 423
            },
            "consignee": {
                "x": 175,
                "y": 423
            },
            "other": {
                "x": 228,
                "y": 423
            },
            "other_please_specify": {
                "x": 380,
                "y": 423
            },
        },



    },

    "items": {
        "item_field": {
            "num_packages": {
                "x": 51,
            },
            "net_weight": {
                "x": 115,
            },
            "weight_uom": {
                "x": 150,
            },
            "hs_number": {
                "x": 360,
            },
            "origin_ctry": {
                "x": 410,
            },
            "description": {
                "x": 250,
            },
            "quantity": {
                "x1": 81,
                "x2": 150
            },
            "unit_price": {
                "x": 462,
            },
            "value": {
                "x": 536,
            },
        },

        "rows": [
            390.5,
            375,
            359.5,
            344,
            328.5,
            313,
            297.5,
            282,
            266.5,
            251,
            235.5,
            214,
            #
            554,
            538.5,
            523.0,
            507.5,
            492.0,
            476.5,
            461.0,
            445.5,
            430.0,
            414.5,
            399.0,
            383.5,
            368.0,
            352.5,
            337.0,
            321.5,
            306.0,
            290.5,
            275.0,
            259.5,
            244.0,
            228.5,
            213.0,
            197.5,
            182.0,
            166.5,
            151.0,
            135.5,
            120.0,
            104.5,
            89.0,
            73.5,
            58.0,

        ]
    },

    "special_instructions": {
        "x": 53,
        "y": 160
    },

    "originator": {
        "x": 77,
        "y": 75
    },


    "totals": {
        "subTotal": {
            "x": 560,
            "y": 192
        },
        "insurance": {
            "x": 560,
            "y": 175
        },
        "freight": {
            "x": 560,
            "y": 158
        },
        "packing": {
            "x": 560,
            "y": 141
        },
        "handling": {
            "x": 560,
            "y": 124
        },
        "other": {
            "x": 560,
            "y": 113
        },
        "Invoice_Total": {
            "x": 560,
            "y": 87
        },
        "currency_code": {
            "x": 560,
            "y": 70
        },
        "next_sub_total": {
            "x": 560,
            "y": 46
        }
    },
}
ddy = -20


def text_center_draw(canvas, x, y, text, font, size, dy=0):
    width = canvas.stringWidth(text=str(text), fontName=font, fontSize=size)
    canvas.setFont(font, size)
    canvas.drawString(x-(width/2), y + 5 + dy, str(text))


pkey_types1 = ["shipment_details", "exporter", "consignee",
               "sold_to", "broker", "special_instructions", "originator", "totals", "items"]


def commericial_invoice_generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 8)

    items = len(data["items"])
    page_cnt = math.ceil((items)/12)  # + #math.ceil((items-12)/32)
    # page 1
    draw_on_page_one(pdf_canvas, data, page_cnt)  # info

    pdf_canvas.save()
    packet.seek(0)
    canvas_page_pdf = PdfReader(packet)
    output = PdfWriter()
    for i in range(page_cnt):
        existing_pdf = PdfReader(
            open("src/commericial_invoice_report/Commercial_Invoice.pdf", "rb"))
        packet.seek(0)
        canvas_page_pdf = PdfReader(packet)
        existing_page = existing_pdf.pages[i]
        existing_page.merge_page(canvas_page_pdf.pages[i])
        output.add_page(existing_page)
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()


def draw_on_page_one(pdf_canvas, data, page_cnt):  # , info):
    for pk in data:
        if pk in pkey_types1:
            if pk == "special_instructions":
                x = position_dict[pk]["x"]
                y = position_dict[pk]["y"]
                val = data[pk]

                text_center_draw(pdf_canvas, x, y-5, val, "Helvetica", 6)
            elif pk == "originator":
                x = position_dict[pk]["x"]
                y = position_dict[pk]["y"]
                val = data[pk]
                text_center_draw(pdf_canvas, x, y-5, val, "Helvetica", 6)
            elif pk == "items":
                draw_items_list(pdf_canvas, data, page_cnt)
            elif pk == "totals":
                pass
            else:
                for key in data[pk]:
                    if key == "parties_to_transaction":
                        for inner_key in data[pk][key]:
                            x = position_dict[pk][key][inner_key]
                            y = position_dict[pk][key]["y"]
                            val = data[pk][key][inner_key]
                            text_center_draw(
                                pdf_canvas, x, y-5, val, "Helvetica", 6)
                    elif key == "duties_taxes_payable_by":
                        for inner_key in data[pk][key]:
                            x = position_dict[pk][key][inner_key]["x"]
                            y = position_dict[pk][key][inner_key]["y"]
                            val = data[pk][key][inner_key]
                            text_center_draw(
                                pdf_canvas, x, y-5, val, "Helvetica", 6)
                    else:
                        x = position_dict[pk][key]["x"]
                        y = position_dict[pk][key]["y"]
                        text_center_draw(pdf_canvas, x, y-5,
                                         str(data[pk][key]), "Helvetica", 6)


def draw_items_list(pdf_canvas, data, page_cnt):
    idx = 0
    item_cnt = len(data["items"])
    # print(page_cnt)
    # Invoice_total = 0
    for i in range(page_cnt):
        # first page
        sub_total = 0
        # print("i", i)
        if i == 0:
            firstPnt = 0
            endPnt = 12
        elif (page_cnt-1) > i > 0:
            firstPnt = 12 + (i-1)*32
            endPnt = i*32 + 12
        elif page_cnt - 1 == i:
            firstPnt = 12 + (i-1)*32
            endPnt = firstPnt + (item_cnt-12) % 32
            # print(idx)
        for item in data["items"]:
            if endPnt > idx >= firstPnt:
                # print("idx", idx)
                for key in item:
                    if key == "quantity":
                        str = data["items"][idx][key]
                        val = str.split(" ")
                        x1 = position_dict["items"]["item_field"][key]["x1"]
                        x2 = position_dict["items"]["item_field"][key]["x2"]
                        y = position_dict["items"]["rows"][idx]
                        text_center_draw(pdf_canvas, x1, y-5,
                                         val[0], "Helvetica", 6)

                    else:
                        if key == "value":
                            sub_total += float(item[key])

                        x = position_dict["items"]["item_field"][key]["x"]
                        y = position_dict["items"]["rows"][idx]
                        val = data["items"][idx][key]
                        # print("val", key , val)
                        text_center_draw(pdf_canvas, x, y-5,
                                         val, "Helvetica", 6)
                        pdf_canvas.line(35, y - 5, 575, y - 5)
                idx += 1
                # total calculation
            else:
                break
        if i == 0:
            first_page_total_Cal(pdf_canvas, data, sub_total)
        else:
            next_page_total_Cal(pdf_canvas, data, sub_total, i)
        pdf_canvas.showPage()


# def first_page_total_Cal(pdf_canvas, data, sub_total):
#     Total_Pkgs = len(data["items"])
#     Total_No_unit = 0
#     Total_netWeight = 0
#     invoice_total = 0
#     # draw page_number
#     text_center_draw(pdf_canvas, 560, 703, "1", "Helvetica", 7)

#     for item in data["items"]:
#         for key in item:
#             if key == "quantity":
#                 strVal = item[key]
#                 val = strVal.split(" ")
#                 Total_No_unit += float(val[0])
#             elif key == "net_weight":
#                 Total_netWeight += float(item["net_weight"])
#             elif key == "value":
#                 invoice_total += float(item["value"])
#     y = position_dict["first_page_total"]["y"]
#     # N of Pkgs
#     x = position_dict["items"]["item_field"]["num_packages"]["x"]
#     text_center_draw(pdf_canvas, x, y, Total_Pkgs, "Helvetica", 6)
#     # quantity
#     x = position_dict["items"]["item_field"]["quantity"]["x1"]
#     text_center_draw(pdf_canvas, x, y, Total_No_unit, "Helvetica", 6)

#     # Net weight
#     x = position_dict["items"]["item_field"]["net_weight"]["x"]
#     text_center_draw(pdf_canvas, x + 10, y, str(Total_netWeight) + "  LBS", "Helvetica", 6)
#     # sub total
#     x = position_dict["totals"]["subTotal"]["x"]
#     y = position_dict["totals"]["subTotal"]["y"]
#     text_center_draw(pdf_canvas, x, y, sub_total, "Helvetica", 6)
#     # invoice total
#     x = position_dict["totals"]["Invoice_Total"]["x"]
#     y = position_dict["totals"]["Invoice_Total"]["y"]
#     text_center_draw(pdf_canvas, x, y, invoice_total, "Helvetica", 6)

#     for pk in data:
#         if pk == "totals":
#             for key in data[pk]:
#                 x = position_dict["totals"][key]["x"]
#                 y = position_dict["totals"][key]["y"]
#                 text_center_draw(pdf_canvas, x, y, data[pk][key], "Helvetica", 6)


def next_page_total_Cal(pdf_canvas, data, sub_total, i):
    # page_number
    text_center_draw(pdf_canvas, 520, 711, i+1, "Helvetica", 7)
    text_center_draw(pdf_canvas, 560, 711, i+1, "Helvetica", 7)
    # exporter
    for pk in data:
        if pk == "exporter":
            for key in data[pk]:
                if key == "company_name" or key == "address1" or key == "address2" or key == "city" or key == "state" or key == "postal_code" or key == "country":
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    # The above code is using the `print` function to output a blank line.
                    # print(pk, key)
                    # print(str(data[pk][key]), key)
                    text_center_draw(pdf_canvas, x, y+55,
                                     str(data[pk][key]), "Helvetica", 6)
        elif pk == "consignee":
            for key in data[pk]:
                if key == "company_name" or key == "address1" or key == "address2" or key == "city" or key == "state" or key == "postal_code" or key == "country":
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    # The above code is using the `print` function to output a blank line.
                    # print(pk, key)
                    # print(str(data[pk][key]), key)
                    text_center_draw(pdf_canvas, x, y+125,
                                     str(data[pk][key]), "Helvetica", 6)
        elif pk == "sold_to":
            for key in data[pk]:
                if key == "company_name" or key == "address1" or key == "address2" or key == "city" or key == "state" or key == "postal_code" or key == "country":
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    # The above code is using the `print` function to output a blank line.
                    # print(pk, key)
                    # print(str(data[pk][key]), key)
                    text_center_draw(pdf_canvas, x, y+125,
                                     str(data[pk][key]), "Helvetica", 6)
        elif pk == "shipment_details":
            for key in data[pk]:
                if key == "track_no" or key == "invoice_number" or key == "po_number" or key == "payment_terms" or key == "bill_of_lading":
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    # The above code is using the `print` function to output a blank line.
                    # print(pk, key)
                    # print(str(data[pk][key]), key)
                    text_center_draw(pdf_canvas, x, y+23,
                                     str(data[pk][key]), "Helvetica", 6)
    # sub total
    x = position_dict["totals"]["next_sub_total"]["x"]
    y = position_dict["totals"]["next_sub_total"]["y"]
    text_center_draw(pdf_canvas, x, y, str(sub_total), "Helvetica", 6)


def first_page_total_Cal(pdf_canvas, data, sub_total):
    Total_Pkgs = 0  # len(data["items"])
    Total_No_unit = 0
    Total_netWeight = 0
    invoice_total = 0
    # draw page_number
    text_center_draw(pdf_canvas, 560, 703, "1", "Helvetica", 7)

    df = pd.DataFrame(data["items"])
    df[['quantity', 'uom']] = df["quantity"].str.split(expand=True)
    df['quantity'] = pd.to_numeric(df['quantity'])
    Total_No_unit = df["quantity"].sum()

    df['num_packages'] = pd.to_numeric(df['num_packages'])
    Total_Pkgs = df["num_packages"].sum()

    df['net_weight'] = pd.to_numeric(df['net_weight'])
    Total_netWeight = df["net_weight"].sum()

    df['value'] = pd.to_numeric(df['value'])
    invoice_total = df["value"].sum()

    y = position_dict["first_page_total"]["y"]
    # N of Pkgs
    x = position_dict["items"]["item_field"]["num_packages"]["x"]
    text_center_draw(pdf_canvas, x, y, Total_Pkgs, "Helvetica", 6)
    # quantity
    x = position_dict["items"]["item_field"]["quantity"]["x1"]
    text_center_draw(pdf_canvas, x, y, Total_No_unit, "Helvetica", 6)

    # Net weight
    x = position_dict["items"]["item_field"]["net_weight"]["x"]
    text_center_draw(pdf_canvas, x + 10, y,
                     str(Total_netWeight) + " LBS", "Helvetica", 6)
    # sub total
    x = position_dict["totals"]["subTotal"]["x"]
    y = position_dict["totals"]["subTotal"]["y"]
    text_center_draw(pdf_canvas, x, y, sub_total, "Helvetica", 6)
    # invoice total
    x = position_dict["totals"]["Invoice_Total"]["x"]
    y = position_dict["totals"]["Invoice_Total"]["y"]
    text_center_draw(pdf_canvas, x, y, invoice_total, "Helvetica", 6)

    for pk in data:
        if pk == "totals":
            for key in data[pk]:
                x = position_dict["totals"][key]["x"]
                y = position_dict["totals"][key]["y"]
                text_center_draw(pdf_canvas, x, y,
                                 data[pk][key], "Helvetica", 6)
