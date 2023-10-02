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
    "ShipFrom": {
        "Name": {
            "x": 85,
            "y": 678
        },
        "Address": {
            "x": 133,
            "y": 664
        },
        "City/State/Zip": {
            "x": 136,
            "y": 650
        },
        "SID#": {
            "x": 84,
            "y": 636
        },
        "FOB": {
            "x": 190,
            "y": 622
        }
    },
    "ShipTo": {

        "Name": {
            "x": 96,
            "y": 606
        }, "Address": {
            "x": 99,
            "y": 592
        }, "City/State/Zip": {
            "x": 126,
            "y": 578
        }, "SID#": {
            "x": 87,
            "y": 564
        }, "FOB": {
            "x": 190,
            "y": 550
        }
    },
    "ThirdParty": {

        "Name": {
            "x": 190,
            "y": 533
        },
        "Address": {
            "x": 190,
            "y": 519
        },
        "City/State/Zip": {
            "x": 190,
            "y": 505
        },
        "SpecialInstructions": {
            "x": 190,
            "y": 487
        },
    },
    "BOL": {
        "BOLNumber": {
            "x": 450,
            "y": 682
        },
        "BarCode": {
            "x": 370,
            "y": 642
        }
    },
    "CarrierDetails": {

        "CarrierName": {
            "x": 420,
            "y": 617
        },
        "TrailerNo": {
            "x": 422,
            "y": 605
        },
        "SealNo": {
            "x": 417,
            "y": 593
        },
        "SCAC": {
            "x": 385,
            "y": 575
        },
        "PRO": {
            "x": 415,
            "y": 563
        },
        "PROBarCode": {
            "Image_x": 370,
            "Image_y": 527,
            "x": 390,
            "y": 518
        },
        "Prepaid": {
            "x": 392,
            "y": 487
        },
        "Collect": {
            "x": 462,
            "y": 487
        },
        "3rdParty": {
            "x": 536,
            "y": 487
        },
        "MasterBOL": {
            "x": 381,
            "y": 471
        },

    },
    "OrderInfo": {
        "page_one_column": {
            "OrderNo": {
                "x": 115,
                "dx": 0,
                "dy": 0
            },
            "Pkgs": {
                "x": 229,
                "dx": 2,
                "dy": 0
            },
            "Weight": {
                "x": 300,
                "dx": 0,
                "dy": 0
            },
            "AddInfo": {
                "x": 490,
                "dx": 0,
                "dy": 0
            },
            "PalletSlip": {
                "Y": 352.5,
                "N": 388.5,
                "dx": 0.5,
                "dy": 1
            },
        },
        "rows": [
            418,
            400,
            382,
            364,
            740,
            722,
            704,
            686,
            668,
            650,
            632,
            614,
            596,
            578,
            560,
            542,
            524,
            506,
            488,
            470,
            452,
            434,
            416,
            398,
            380,
            362,
            344,
            326,
            308,
            290,
            272,
            254,
            236,
            218,
            200,
            182,
            164,
            146,
            128,
            110,
            92,
            74,
            56,
            38
        ]
    },
    "CarrierInfo": {
        "page_one_column": {
            "HUQty": {
                "x": 55,
                "dy": 0
            },
            "HUType": {
                "x": 90,
                "dy": 0
            },
            "PkgQty": {
                "x": 127,
                "dy": 0
            },
            "PkgType": {
                "x": 163,
                "dy": 0
            },
            "Weight": {
                "x": 210,
                "dy": 0
            },
            "HM": {
                "x": 254,
                "dy": 0
            },
            "Desc": {
                "x": 380,
                "dy": 0
            },
            "NMFC": {
                "x": 510,
                "dy": 0
            },
            "Class": {
                "x": 555,
                "dy": 0
            },
        },
        "page_two_column": {
            "HUQty": {
                "x": 55
            },
            "HUType": {
                "x": 90
            },
            "PkgQty": {
                "x": 127
            },
            "PkgType": {
                "x": 163
            },
            "Weight": {
                "x": 210
            },
            "HM": {
                "x": 254
            },
            "Desc": {
                "x": 380
            },
            "NMFC": {
                "x": 510
            },
            "Class": {
                "x": 555
            },
        },
        "rows": [
            282,
            264,
            246,
            228,
            210,
            740,
            722,
            704,
            686,
            668,
            650,
            632,
            614,
            596,
            578,
            560,
            542,
            524,
            506,
            488,
            470,
            452,
            434,
            416,
            398,
            380,
            362,
            344,
            326,
            308,
            290,
            272,
            254,
            236,
            218,
            200,
            182,
            164,
            146,
            128,
            110,
            92,
            74,
            56,
            38
        ],
        "sub_total": 32
    },
    "Footer": {
        "DeclaredValue": {
            "x": 72,
            "y": 146
        },
        "DeclaredValuePer": {
            "x": 150,
            "y": 146
        },
        "CODAmount": {
            "x": 485,
            "y": 172
        },
        "Collect": {
            "x": 464,
            "y": 161
        },
        "Prepaid": {
            "x": 531,
            "y": 161
        },
        "CustCheck": {
            "x": 514,
            "y": 147
        },
        "TLByShipper": {
            "x": 232,
            "y": 72
        },
        "TLByDriver": {
            "x": 232,
            "y": 58
        },
        "FCByShipper": {
            "x": 295,
            "y": 71
        },
        "FCByDriverContains": {
            "x": 295,
            "y": 56
        },
        "FCByDriverPieces": {
            "x": 295,
            "y": 41
        }
    }
}
ddy = -20


def text_center_draw(canvas, x, y, text, font, size, dy=0):
    width = canvas.stringWidth(text=text, fontName=font, fontSize=size)
    canvas.setFont(font, size)
    canvas.drawString(x-(width/2), y + 5 + dy, text)


pkey_types1 = ["ShipFrom", "ShipTo", "ThirdParty",
               "BOL", "CarrierDetails", "Footer"]


def vict_stand_generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 8)

    info = extract_additional_information(data)

    # page 1
    draw_on_page_one(pdf_canvas, data, info)

    # items = max(len(data["OrderInfo"]["Items"]), len(data["CarrierInfo"]["Items"]))
    items = len(data["OrderInfo"]["Items"])
    # calculate the total page count
    page_cnt = math.ceil((items-4)/34)

    for i in range(page_cnt):
        draw_new_page(pdf_canvas, draw_page, data)

        pdf_canvas.setFont("Helvetica", 8)
        x = position_dict["next_page_number"]["x"]
        y = position_dict["next_page_number"]["y"]
        text_center_draw(pdf_canvas, x, y, str(i+2), "Helvetica", 15, ddy)
        endpoint = (i+1) * 34 + 4
        firstpoint = i*34 + 3
        # order sub total
        sub_Pkgs_total = 0
        sub_Order_weight_total = 0

        for pk in data:
            if pk == "OrderInfo":
                idx = 0
                radius = 7
                customer_order_header(pdf_canvas, ddy)
                # pdf_canvas.line(418, 679, 418, 668)
                for row_data in data[pk]['Items']:
                    if endpoint > idx > firstpoint:
                        for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                            val = row_data[key]
                            dx = position_dict["OrderInfo"]["page_one_column"][key]["dx"]
                            dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                            y = position_dict["OrderInfo"]["rows"][idx - i*34 + 5]
                            pdf_canvas.setFont("Helvetica", 8)
                            pdf_canvas.line(40, y + ddy, 570, y + ddy)

                            draw_stick_customer(pdf_canvas, y, ddy)

                            text_center_draw(
                                pdf_canvas, 353, y, "Y", "Helvetica", 8, ddy)
                            text_center_draw(
                                pdf_canvas, 388, y, "N", "Helvetica", 8, ddy)

                            # sub total
                            if key == "Pkgs":
                                sub_Pkgs_total += float(val)
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(
                                    pdf_canvas, x - dx, y + dy, val, "Helvetica", 8, ddy)
                            elif key == "Weight":
                                sub_Order_weight_total += float(val)
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(
                                    pdf_canvas, x - dx, y + dy, val, "Helvetica", 8, ddy)
                            elif key == "PalletSlip":
                                x = position_dict["OrderInfo"]["page_one_column"][key][val]
                                pdf_canvas.circle(x, y + 8.5 + ddy, radius)
                            else:
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(
                                    pdf_canvas, x - dx, y + dy, val, "Helvetica", 8, ddy)
                    idx += 1

        x = position_dict["OrderInfo"]["page_one_column"]["Pkgs"]["x"]

        if (items - i * 34 - 4) > 34:
            y = position_dict["OrderInfo"]["rows"][43]
            draw_stick_customer(pdf_canvas, y, ddy)
            custom_order_total(
                pdf_canvas, x, y + ddy, sub_Pkgs_total, sub_Order_weight_total)
        # last of customer order info.
        elif (items - i * 34 - 4) < 34:
            idx = (items - i*34 - 4) % 34
            # print(idx)
            y = position_dict["OrderInfo"]["rows"][idx+5+4]
            draw_stick_customer(pdf_canvas, y, ddy)
            custom_order_total(
                pdf_canvas, x, y + ddy, sub_Pkgs_total, sub_Order_weight_total)
            # carrier information items //total
            carrier_information(data, pdf_canvas, idx+7, ddy)
        pdf_canvas.showPage()
    # all canvas page save.
    pdf_canvas.save()
    packet.seek(0)
    canvas_page_pdf = PdfReader(packet)

    existing_pdf = PdfReader(
        open("src/vict_stand_report/vics-stand.pdf", "rb"))
    output = PdfWriter()
    first_page = existing_pdf.pages[0]
    first_page.merge_page(canvas_page_pdf.pages[0])
    output.add_page(first_page)

    # adding rest of page to output.
    for i in range(page_cnt):
        existing_pdf = PdfReader(
            open("src/vict_stand_report/vics-stand.pdf", "rb"))
        packet.seek(0)
        canvas_page_pdf = PdfReader(packet)
        second_page = existing_pdf.pages[1]
        second_page.merge_page(canvas_page_pdf.pages[i + 1])
        output.add_page(second_page)
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()


def draw_on_page_one(pdf_canvas, data, info):
    Pkgs_total = info['pkgs']['total']
    Pkg_qty_total = info['pkgs']['qty_total']
    Order_weight_total = info['order_weight_total']
    HU_qty_total = info['HU_qty_total']
    Weight_total = info['weight_total']

    # page number
    x = position_dict["first_page_number"]["x"]
    y = position_dict["first_page_number"]["y"]
    text_center_draw(pdf_canvas, x, y, "1", "Helvetica", 15)

    for pk in data:
        if pk in pkey_types1:
            for key in data[pk]:
                x = position_dict[pk][key]["x"]
                y = position_dict[pk][key]["y"]
                if key == "BarCode":
                    # generate barcode
                    code128 = barcode.Code128(
                        str(data[pk][key]), writer=ImageWriter())
                    filename = "dist/Barcode"
                    code128.save(filename)
                    image = Image.open("dist/BarCode.png")
                    # Remove the text portion by cropping the image
                    cropped_image = image.crop(
                        (0, 0, image.width, image.height - 90))
                    # Adjust the cropping dimensions as needed
                    # Save the modified image without the barcode number
                    cropped_image.save("dist/BarCode_noText.png")
                    # draw the barcode image onto the canvas
                    barcode_width = 150
                    barcode_height = 32
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    filename = "dist/Barcode_noText.png"
                    pdf_canvas.drawImage(
                        filename, x, y, width=barcode_width, height=barcode_height)
                elif key == "PROBarCode":
                    code128 = barcode.get('code128', str(
                        data[pk][key]), writer=ImageWriter())
                    filename = "dist/PROBarCode"
                    code128.save(filename)
                    image = Image.open("dist/PROBarCode.png")
                    # Remove the text portion by cropping the image
                    cropped_image = image.crop(
                        (0, 0, image.width, image.height - 90))
                    # Adjust the cropping dimensions as needed
                    # Save the modified image without the barcode number
                    cropped_image.save("dist/PROBarCode_noText.png")
                    # draw the barcode image onto the canvas
                    barcode_width = 150
                    barcode_height = 32
                    image_x = position_dict[pk][key]["Image_x"]
                    image_y = position_dict[pk][key]["Image_y"]
                    filename = "dist/PROBarCode_noText.png"
                    pdf_canvas.drawImage(
                        filename, image_x, image_y, width=barcode_width, height=barcode_height)
                else:
                    text_center_draw(pdf_canvas, x, y-5,
                                     data[pk][key], "Helvetica", 8)
        elif pk == "OrderInfo":
            idx = 0
            radius = 7

            for row_data in data[pk]['Items']:
                if idx < 4:
                    for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                        val = row_data[key]
                        dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                        y = position_dict["OrderInfo"]["rows"][idx]

                        if key == "PalletSlip":
                            x = position_dict["OrderInfo"]["page_one_column"][key][val]
                            pdf_canvas.circle(x, y + 3, radius)
                        else:
                            x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                            text_center_draw(
                                pdf_canvas, x, y-5, val, "Helvetica", 8)
                else:
                    break
                idx += 1
        elif pk == "CarrierInfo":
            idx = 0

            for row_data in data[pk]['Items']:
                if idx < 5:
                    for key in ["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"]:
                        val = row_data[key]
                        x = position_dict[pk]["page_one_column"][key]["x"]
                        dy = position_dict[pk]["page_one_column"][key]["dy"]
                        y = position_dict[pk]["rows"][idx]
                        text_center_draw(pdf_canvas, x, y-5,
                                         val, "Helvetica", 8)
                else:
                    break
                idx += 1

    x = position_dict["OrderInfo"]["page_one_column"]["Pkgs"]["x"]
    y = position_dict["OrderInfo"]["rows"][3]
    text_center_draw(pdf_canvas, x, y - 23, str(Pkgs_total), "Helvetica", 8)
    x = position_dict["OrderInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x, y - 23,
                     str(Order_weight_total), "Helvetica", 8)
    # carrier info
    x = position_dict["CarrierInfo"]["page_one_column"]["HUQty"]["x"]
    y = position_dict["CarrierInfo"]["rows"][4]
    text_center_draw(pdf_canvas, x, y - 23, str(HU_qty_total), "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["PkgQty"]["x"]
    text_center_draw(pdf_canvas, x, y - 23, str(Pkg_qty_total), "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x, y - 23, str(Weight_total), "Helvetica", 8)
    pdf_canvas.showPage()
    pdf_canvas.setFont("Helvetica", 8)


def extract_additional_information(data):
    Pkgs_total = 0
    Order_weight_total = 0
    HU_qty_total = 0
    Pkg_qty_total = 0
    Weight_total = 0

    for pk in data:
        if pk == "OrderInfo":
            for row_data in data[pk]['Items']:
                Pkgs_total += float(row_data["Pkgs"])
                Order_weight_total += float(row_data["Weight"])
        elif pk == "CarrierInfo":
            for row_data in data[pk]['Items']:
                HU_qty_total += float(row_data["HUQty"])
                Pkg_qty_total += float(row_data["PkgQty"])
                Weight_total += float(row_data["Weight"].split(" ")[0])

    return {
        'pkgs': {
            'total': round(Pkgs_total, 2),
            'qty_total': round(Pkg_qty_total, 2),
        },
        'weight_total': round(Weight_total, 2),
        'order_weight_total': round(Order_weight_total, 2),
        'HU_qty_total': round(HU_qty_total, 2),
    }


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


def draw_stick_customer(pdf_canvas, y, dy):
    pdf_canvas.line(190, y + 18 + dy, 190, y + dy)
    pdf_canvas.line(263, y + 18 + dy, 263, y + dy)
    pdf_canvas.line(335, y + 18 + dy, 335, y + dy)
    pdf_canvas.line(405, y + 18 + dy, 405, y + dy)
    pdf_canvas.line(370, y + 18 + dy, 370, y + dy)

    pdf_canvas.line(40, y + 18 + dy, 40, y + dy)
    pdf_canvas.line(570, y + 18 + dy, 570, y + dy)


def custom_order_total(pdf_canvas, x, y, sub_Pkgs_total, sub_Order_weight_total):
    text_center_draw(pdf_canvas, x, y, str(sub_Pkgs_total), "Helvetica", 8)
    x = position_dict["OrderInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x, y, str(
        round(sub_Order_weight_total, 2)), "Helvetica", 8)
    pdf_canvas.setFillColor(lightslategray)
    pdf_canvas.rect(40, y, 150, 18, fill=1)
    pdf_canvas.rect(335, y, 40, 18, fill=1)
    pdf_canvas.rect(370, y, 40, 18, fill=1)
    pdf_canvas.rect(405, y, 165, 18, fill=1)
    pdf_canvas.setFillColor(black)
    pdf_canvas.line(40, y, 570, y)


def carrier_information(data, pdf_canvas, idx, ddy):  # 10
    # carrier sub total
    sub_hu_qty_total = 0
    sub_pkg_qty_total = 0
    sub_weight_total = 0
    items = len(data["CarrierInfo"]["Items"])
    # calculate the total page count
    page_cnt = math.ceil((items-5+idx)/34)
    # print("item_counts", items)
    for i in range(page_cnt):
        if i == 0:
            firstpoint = i*34 + 4
            endpoint = (i+1) * 34 - idx + 5
            y = position_dict["CarrierInfo"]["rows"][idx+4] + ddy
            carrier_info_header(pdf_canvas, y)
        else:
            firstpoint = i*34 - (idx + 2) + 3
            endpoint = (i+1)*33-(idx + 2)+4
            draw_new_page(pdf_canvas, draw_page, data, ddy)

            x = position_dict["next_page_number"]["x"]
            y = position_dict["next_page_number"]["y"]
            text_center_draw(pdf_canvas, x, y, str(i+2), "Helvetica", 15, ddy)

            sub_hu_qty_total = 0
            sub_pkg_qty_total = 0
            sub_weight_total = 0

            y = 680 + dy + ddy
            carrier_info_header(pdf_canvas, y)

        for pk in data:
            if pk == "CarrierInfo":
                id = 0
                for row_data in data[pk]['Items']:
                    for key in ["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"]:
                        if endpoint > id > firstpoint:
                            val = row_data[key]
                            x = position_dict[pk]["page_one_column"][key]["x"]
                            dy = position_dict[pk]["page_one_column"][key]["dy"]
                            if i == 0:
                                y = position_dict[pk]["rows"][id+idx+2]
                            else:
                                y = position_dict[pk]["rows"][id-i*34+5]
                            draw_stick_carrier(pdf_canvas, y + ddy)
                            text_center_draw(
                                pdf_canvas, x, y + dy, val, "Helvetica", 8, ddy)
                            if key == "HUQty":
                                sub_hu_qty_total += float(val)
                            elif key == "PkgQty":
                                sub_pkg_qty_total += float(val)
                            elif key == "Weight":
                                sub_weight_total += float(val.split(" ")[0])
                    id += 1
        # carrier info
        x = position_dict["CarrierInfo"]["page_one_column"]["HUQty"]["x"]
        # y = position_dict["CarrierInfo"]["sub_total"]
        val = str(round(sub_hu_qty_total, 2))
        if (items - i * 34 - 5) > 34:
            y = position_dict["OrderInfo"]["rows"][43] + ddy
            carrier_info_total(pdf_canvas, x, y, val,
                               sub_pkg_qty_total, sub_weight_total)
            draw_stick_carrier(pdf_canvas, y-18)
        elif (items - i * 34 - 5) < 34:
            id = (items - i * 34 - 5) % 34
            # print("index", i, id, idx)
            y = position_dict["OrderInfo"]["rows"][(id+idx+5)] + ddy
            carrier_info_total(pdf_canvas, x, y, val,
                               sub_pkg_qty_total, sub_weight_total)
            draw_stick_carrier(pdf_canvas, y-18)
        pdf_canvas.showPage()


def carrier_info_total(pdf_canvas, x, y, val, sub_pkg_qty_total, sub_weight_total):
    text_center_draw(pdf_canvas, x, y-18, val, "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["PkgQty"]["x"]
    text_center_draw(pdf_canvas, x, y-18,
                     str(sub_pkg_qty_total), "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x, y-18,
                     str(sub_weight_total), "Helvetica", 8)
    pdf_canvas.setFillColor(lightslategray)
    pdf_canvas.rect(75, y - 18, 35, 18, fill=1)
    pdf_canvas.rect(145, y - 18, 37, 18, fill=1)
    pdf_canvas.rect(235, y - 18, 335, 18, fill=1)

    pdf_canvas.setFillColor(black)


def carrier_info_header(pdf_canvas, y):

    # pdf_canvas.line(40, y, 570, y)

    # pdf_canvas.line(40, y+18, 40, y)
    # pdf_canvas.line(570, y+18, 570, y)
    pdf_canvas.setFillColor(black)
    pdf_canvas.rect(40, y, 530, 18, fill=1)
    pdf_canvas.setFillColor(white)

    text_center_draw(pdf_canvas, 310, y+2,
                     "CARRIER INFORMATION", "Helvetica", 8)
    pdf_canvas.setFillColor(black)
    # pdf_canvas.setFillColor(white)
    # pdf_canvas.setStrokeColor(black)
    text_center_draw(pdf_canvas, 75, y-18, "HANDLING UNIT", "Helvetica", 8)
    text_center_draw(pdf_canvas, 145, y-18, "PACKAGE", "Helvetica", 8)
    text_center_draw(pdf_canvas, 210, y-22, "WEIGHT", "Helvetica", 8)
    text_center_draw(pdf_canvas, 250, y-22, "H.M.X", "Helvetica", 8)
    text_center_draw(pdf_canvas, 375, y-22,
                     "COMMODITY DESCRIPTION.", "Helvetica", 8)
    text_center_draw(pdf_canvas, 530, y-18, "LTL ONLY", "Helvetica", 8)
    pdf_canvas.line(40, y-18, 182, y-18)
    pdf_canvas.line(480, y-18, 570, y-18)

    pdf_canvas.line(40, y, 40, y-36)
    pdf_canvas.line(570, y, 570, y-36)
    pdf_canvas.line(110, y, 110, y-36)
    pdf_canvas.line(182, y, 182, y-36)
    pdf_canvas.line(235, y, 235, y-36)
    pdf_canvas.line(265, y, 265, y-36)
    pdf_canvas.line(480, y, 480, y-36)

    # 1 down
    y = y-18
    pdf_canvas.line(75, y, 75, y-18)
    pdf_canvas.line(145, y, 145, y-18)
    pdf_canvas.line(540, y, 540, y-18)

    pdf_canvas.line(40, y-18, 570, y-18)

    text_center_draw(pdf_canvas, 56, y-18, "QTY", "Helvetica", 8)
    text_center_draw(pdf_canvas, 93, y-18, "TYPE", "Helvetica", 8)
    text_center_draw(pdf_canvas, 126, y-18, "QTY", "Helvetica", 8)
    text_center_draw(pdf_canvas, 165, y-18, "TYPE", "Helvetica", 8)
    text_center_draw(pdf_canvas, 510, y-18, "NMFC #", "Helvetica", 8)
    text_center_draw(pdf_canvas, 555, y-18, "CLASS", "Helvetica", 8)


def draw_stick_carrier(pdf_canvas, y):
    pdf_canvas.line(75, y+18, 75, y)
    pdf_canvas.line(145, y+18, 145, y)
    pdf_canvas.line(540, y+18, 540, y)

    pdf_canvas.line(40, y+18, 40, y)
    pdf_canvas.line(570, y+18, 570, y)
    pdf_canvas.line(110, y+18, 110, y)
    pdf_canvas.line(182, y+18, 182, y)
    pdf_canvas.line(235, y+18, 235, y)
    pdf_canvas.line(265, y+18, 265, y)
    pdf_canvas.line(480, y+18, 480, y)

    pdf_canvas.line(40, y, 570, y)


def customer_order_header(pdf_canvas, dy):
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.line(40, 686 + dy, 570, 686 + dy)

    pdf_canvas.line(40, 740 + dy, 40, 686 + dy)
    pdf_canvas.line(570, 740 + dy, 570, 686 + dy)

    pdf_canvas.setFillColor(black)
    pdf_canvas.rect(40, 685 + dy, 530, 14, fill=1)
    pdf_canvas.setFillColor(white)
    text_center_draw(pdf_canvas, 300, 685,
                     "CUSTOMER ORDER INFORMATION", "Helvetica", 8, dy)
    pdf_canvas.setFillColor(black)
    text_center_draw(pdf_canvas, 115, 670,
                     "CUSTOMER ORDER NUMBER", "Helvetica", 8, dy)
    text_center_draw(pdf_canvas, 228, 670, "# PKGS", "Helvetica", 8, dy)
    text_center_draw(pdf_canvas, 300, 670, "WEIGHT", "Helvetica", 8, dy)
    text_center_draw(pdf_canvas, 370, 670, "PALLET/SLIP", "Helvetica", 8, dy)
    text_center_draw(pdf_canvas, 490, 670,
                     "ADDITIONAL SHIPPER INFO.", "Helvetica", 8, dy)

    pdf_canvas.line(40, 668 + dy, 570, 668 + dy)

    pdf_canvas.line(190, 686 + dy, 190, 668 + dy)
    pdf_canvas.line(263, 686 + dy, 263, 668 + dy)
    pdf_canvas.line(335, 686 + dy, 335, 668 + dy)
    pdf_canvas.line(405, 686 + dy, 405, 668 + dy)

    pdf_canvas.line(40, 686 + dy, 40, 668 + dy)
    pdf_canvas.line(570, 686 + dy, 570, 668 + dy)
