from PyPDF2 import PdfWriter, PdfReader
import io
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import barcode
from barcode.writer import ImageWriter
from PIL import Image
# Array
draw_page = {
    "edge": {
        "x1": 40,
        "x2": 570,
        "y1": 740,
        "y2": 30
    }
    
}
position_dict = {
    "first_page_number": {
        "x": 550,
        "y": 707
    },
    "next_page_number":{
        "x": 550,
        "y": 725
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
            654,
            636,
            618,
            600,
            582,
            564,
            546,
            528,
            510,
            492,
            473,
            456,
            438,
            420,
            402,
            384,
            366,
            348,
            330,
            312,
            294,
            276,
            258,
            240,
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
            322,
            304,
            286,
            268,
            250,
            232,
            214,
            196,
            178,
            160,
            142,
            124,
            104,
            86,
            68,
            50,
            32,
            14
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

def text_center_draw(canvas, x, y, text, font, size):
    width = canvas.stringWidth(text=text, fontName=font, fontSize=size)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(x-(width/2), y, text)

pkey_types1 = ["ShipFrom", "ShipTo", "ThirdParty", "BOL", "CarrierDetails", "Footer"]

def generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)
    data = json.loads(json_data)
    packet = io.BytesIO()

    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 8)

    x = position_dict["first_page_number"]["x"]
    y = position_dict["first_page_number"]["y"]
    text_center_draw(pdf_canvas, x, y, "1", "Helvetica", 35)
    for pk in data:
        if pk in pkey_types1:
            for key in data[pk]:
                x = position_dict[pk][key]["x"]
                y = position_dict[pk][key]["y"]
                if key == "BarCode":
                    #generate barcode                 
                    code128 = barcode.Code128(str(data[pk][key]), writer=ImageWriter())
                    filename = "Barcode"
                    code128.save(filename)
                    image = Image.open("BarCode.png")
                    # Remove the text portion by cropping the image
                    cropped_image = image.crop((0, 0, image.width, image.height - 90))  
                    # Adjust the cropping dimensions as needed
                    # Save the modified image without the barcode number
                    cropped_image.save("BarCode_noText.png")
                    #draw the barcode image onto the canvas
                    barcode_width = 150
                    barcode_height = 32
                    x = position_dict[pk][key]["x"]
                    y = position_dict[pk][key]["y"]
                    filename = "Barcode_noText.png"
                    pdf_canvas.drawImage(filename, x, y, width=barcode_width, height=barcode_height)
                elif key == "PROBarCode":
                    code128 = barcode.get('code128', str(data[pk][key]), writer=ImageWriter())
                    filename = "PROBarCode"
                    code128.save(filename)
                    image = Image.open("PROBarCode.png")
                    # Remove the text portion by cropping the image
                    cropped_image = image.crop((0, 0, image.width, image.height - 90))  
                    # Adjust the cropping dimensions as needed
                    # Save the modified image without the barcode number
                    cropped_image.save("PROBarCode_noText.png")
                    #draw the barcode image onto the canvas
                    barcode_width = 150
                    barcode_height = 32
                    image_x = position_dict[pk][key]["Image_x"]
                    image_y = position_dict[pk][key]["Image_y"]
                    filename = "PROBarCode_noText.png"
                    pdf_canvas.drawImage(filename, image_x, image_y, width=barcode_width, height=barcode_height)  
                else:
                    text_center_draw(pdf_canvas, x, y, data[pk][key], "Helvetica", 8)
        if pk == "OrderInfo":
            idx = 0
            radius = 7
            Pkgs_total = 0
            Order_weight_total = 0
            for row_data in data[pk]['Items']:
                for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                    val = row_data[key]
                    if idx < 4:
                        dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                        y = position_dict["OrderInfo"]["rows"][idx]
                        if key == "Pkgs":
                            Pkgs_total += float(val)
                        if key == "Weight":
                            Order_weight_total += float(val)
                        if key == "PalletSlip":
                            x = position_dict["OrderInfo"]["page_one_column"][key][val]
                            pdf_canvas.circle(x, y + 3, radius)
                        else:
                            x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                            text_center_draw(pdf_canvas, x, y + dy, val, "Helvetica", 8)
                    else: 
                        if key == "Pkgs":
                            Pkgs_total += float(val)
                        if key == "Weight":
                            Order_weight_total += float(val)
                idx += 1
        elif pk == "CarrierInfo":
            idx = 0
            HU_qty_total = 0
            Pkg_qty_total = 0
            Weight_total = 0
            for row_data in data[pk]['Items']:
                for key in ["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"]:
                    val = row_data[key]
                    if idx < 5:
                        x = position_dict[pk]["page_one_column"][key]["x"]
                        dy = position_dict[pk]["page_one_column"][key]["dy"]
                        y = position_dict[pk]["rows"][idx]
                        text_center_draw(pdf_canvas, x, y + dy, val, "Helvetica", 8)
                        if key == "HUQty":
                            HU_qty_total += float(val)
                        if key == "PkgQty":
                            Pkg_qty_total += float(val)
                        if key == "Weight":
                            Weight_total += float(val.split(" ")[0])
                    else:
                        if key == "HUQty":
                            HU_qty_total += float(val)
                        if key == "PkgQty":
                            Pkg_qty_total += float(val)
                        if key == "Weight":
                            Weight_total += float(val.split(" ")[0])
                idx += 1
    #order info
    x = position_dict["OrderInfo"]["page_one_column"]["Pkgs"]["x"]
    y = position_dict["OrderInfo"]["rows"][3]
    text_center_draw(pdf_canvas, x , y - 18, str(Pkgs_total), "Helvetica", 8)
    x = position_dict["OrderInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x , y - 18, str(Order_weight_total), "Helvetica", 8)
    #carrier info            
    x = position_dict["CarrierInfo"]["page_one_column"]["HUQty"]["x"]
    y = position_dict["CarrierInfo"]["rows"][4]
    text_center_draw(pdf_canvas, x , y - 18, str(HU_qty_total), "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["PkgQty"]["x"]
    text_center_draw(pdf_canvas, x , y - 18, str(Pkg_qty_total), "Helvetica", 8)
    x = position_dict["CarrierInfo"]["page_one_column"]["Weight"]["x"]
    text_center_draw(pdf_canvas, x , y - 18, str(Weight_total), "Helvetica", 8)
    # go to next page

    #page drawing
    


    pdf_canvas.showPage()
    pdf_canvas.setFont("Helvetica", 8)

    x1 = draw_page["edge"]["x1"]
    x2 = draw_page["edge"]["x2"]
    y1 = draw_page["edge"]["y1"]
    y2 = draw_page["edge"]["y2"]
    pdf_canvas.line(x1, y1, x2, y1)
    pdf_canvas.line(x1, y1, x1, y2)
    pdf_canvas.line(x1, y2, x2, y2)
    pdf_canvas.line(x2, y2, x2, y1)

    
    text_center_draw(pdf_canvas, 55 , 722, "Date:", "Helvetica", 8)
    pdf_canvas.setFont("Helvetica", 14)
    text_center_draw(pdf_canvas, 370 , 722, "SUPPLEMENT TO THE BILL OF LADING", "Helvetica", 20)
    pdf_canvas.setFont("Helvetica", 8)
    text_center_draw(pdf_canvas, 500 , 722, "Page", "Helvetica", 8)
    pdf_canvas.line(520, 722, 560, 722)

    text_center_draw(pdf_canvas, 350 , 700, "Bill of Lading Number", "Helvetica", 8)
    pdf_canvas.line(420, 700, 560, 700)

    # items = max(len(data["OrderInfo"]["Items"]), len(data["CarrierInfo"]["Items"]))
    items = len(data["OrderInfo"]["Items"])
    page_cnt = math.ceil((items-4)/38)
    for i in range(page_cnt):
        pdf_canvas.setFont("Helvetica", 8)
        x = position_dict["next_page_number"]["x"]
        y = position_dict["next_page_number"]["y"]
        text_center_draw(pdf_canvas, x, y, str(i+2), "Helvetica", 35)

        endpoint = (i+1) * 38 + 3
        firstpoint = i*38 + 3
        #order sub total
        sub_Pkgs_total = 0
        sub_Order_weight_total = 0
        #carrier sub total
        sub_hu_qty_total = 0
        sub_pkg_qty_total = 0
        sub_weight_total = 0
        for pk in data:
            if pk == "OrderInfo":
                idx = 0
                radius = 7
                pdf_canvas.setFont("Helvetica", 8)
                text_center_draw(pdf_canvas, 400 , 680, "CUSTOMER ORDER INFORMATION", "Helvetica", 20)
                pdf_canvas.line(40, 679, 570, 679)
                
                text_center_draw(pdf_canvas, 115, 670, "CUSTOMER ORDER NUMBER", "Helvetica", 8)
                text_center_draw(pdf_canvas, 225, 670, "# PKGS", "Helvetica", 8)
                text_center_draw(pdf_canvas, 300, 670, "WEIGHT", "Helvetica", 8)
                text_center_draw(pdf_canvas, 370, 670, "PALLET/SLIP", "Helvetica", 8)
                text_center_draw(pdf_canvas, 490, 670, "ADDITIONAL SHIPPER INFO.", "Helvetica", 8)

                pdf_canvas.line(40, 666, 570, 666)
                
                pdf_canvas.line(190, 679, 190, 666)
                pdf_canvas.line(263, 679, 263, 666)
                pdf_canvas.line(335, 679, 335, 666)
                pdf_canvas.line(405, 679, 405, 666)

                # pdf_canvas.line(418, 679, 418, 668)
                
                


                for row_data in data[pk]['Items']:
                    if endpoint + 1 > idx > firstpoint:
                        for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                            val = row_data[key]
                            dx = position_dict["OrderInfo"]["page_one_column"][key]["dx"]
                            dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                            y = position_dict["OrderInfo"]["rows"][idx-i*38]
                            pdf_canvas.setFont("Helvetica", 8)
                            pdf_canvas.line(40, y - 6, 570, y - 6)

                            pdf_canvas.line(190, y + 12, 190, y - 6)
                            pdf_canvas.line(263, y + 12, 263, y - 6)
                            pdf_canvas.line(335, y + 12, 335, y - 6)
                            pdf_canvas.line(405, y + 12, 405, y - 6)
                            pdf_canvas.line(370, y + 12, 370, y - 6)

                            text_center_draw(pdf_canvas, 353, y, "Y", "Helvetica", 8)
                            text_center_draw(pdf_canvas, 388, y, "N", "Helvetica", 8)

                            #sub total
                            if key == "Pkgs":
                                sub_Pkgs_total += float(val)
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(pdf_canvas, x - dx, y + dy, val, "Helvetica", 8)
                            elif key == "Weight":
                                sub_Order_weight_total += float(val)
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(pdf_canvas, x - dx, y + dy, val, "Helvetica", 8)
                            elif key == "PalletSlip":
                                x = position_dict["OrderInfo"]["page_one_column"][key][val]
                                pdf_canvas.circle(x, y + 3, radius)
                            else:
                                x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                                text_center_draw(pdf_canvas, x - dx, y + dy, val, "Helvetica", 8)
                    idx += 1
                #order info
                x = position_dict["OrderInfo"]["page_one_column"]["Pkgs"]["x"]
                y = position_dict["OrderInfo"]["rows"][18]
                text_center_draw(pdf_canvas, x , y - 18, str(sub_Pkgs_total), "Helvetica", 8)

                x = position_dict["OrderInfo"]["page_one_column"]["Weight"]["x"]
                text_center_draw(pdf_canvas, x , y - 18, str(round(sub_Order_weight_total, 2)), "Helvetica", 8)
            # elif pk == "CarrierInfo":
            #     idx = 0
            #     for row_data in data[pk]['Items']:
            #         for key in ["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"]:
            #             val = row_data[key]
            #             if endpoint+3 > idx > firstpoint+1+i:
            #                 print(i, idx)
            #                 x = position_dict[pk]["page_one_column"][key]["x"]
            #                 dy = position_dict[pk]["page_one_column"][key]["dy"]
            #                 y = position_dict[pk]["rows"][idx - i*16]
            #                 text_center_draw(pdf_canvas, x, y + dy, val, "Helvetica", 8)
            #                 if key == "HUQty":
            #                     sub_hu_qty_total += float(val)
            #                 elif key == "PkgQty": 
            #                     sub_pkg_qty_total += float(val)
            #                 elif key == "Weight":
            #                     sub_weight_total += float(val.split(" ")[0])
            #         idx += 1
            #     #carrier info            
            #     x = position_dict["CarrierInfo"]["page_one_column"]["HUQty"]["x"]
            #     y = position_dict["CarrierInfo"]["sub_total"]
            #     val = str(round(sub_hu_qty_total, 2))
            #     text_center_draw(pdf_canvas, x , y, val, "Helvetica", 8)
            #     x = position_dict["CarrierInfo"]["page_one_column"]["PkgQty"]["x"]
            #     text_center_draw(pdf_canvas, x , y, str(sub_pkg_qty_total), "Helvetica", 8)
            #     x = position_dict["CarrierInfo"]["page_one_column"]["Weight"]["x"]
            #     text_center_draw(pdf_canvas, x , y, str(sub_weight_total), "Helvetica", 8)
        pdf_canvas.showPage()
    # all canvas page save.
    pdf_canvas.save()
    packet.seek(0)
    canvas_page_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open("vics-stand.pdf", "rb"))
    output = PdfWriter()
    first_page = existing_pdf.pages[0]
    first_page.merge_page(canvas_page_pdf.pages[0])
    output.add_page(first_page)
    #adding rest of page to output.
    for i in range(page_cnt):
        packet.seek(0)
        canvas_page_pdf = PdfReader(packet)
        # existing_pdf = PdfReader(open("vics-stand.pdf", "rb"))
        # next_page = existing_pdf.pages[1]
        # next_page.merge_page(canvas_page_pdf.pages[i + 1])
        output.add_page(canvas_page_pdf.pages[i + 1])
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()


