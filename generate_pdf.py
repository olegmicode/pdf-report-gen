from PyPDF2 import PdfWriter, PdfReader
import io
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily('Vera', normal='Vera', bold='',
                   italic='VeraIt', boldItalic='VeraBI')
# Array
position_dict = {
    "ShipFrom": {
        "Name": {
            "x": 190,
            "y": 678
        },
        "Address": {
            "x": 190,
            "y": 664
        },
        "City/State/Zip": {
            "x": 190,
            "y": 650
        },
        "SID#": {
            "x": 190,
            "y": 636
        },
        "FOB": {
            "x": 190,
            "y": 622
        }
    },
    "ShipTo": {

        "Name": {
            "x": 190,
            "y": 606
        }, "Address": {
            "x": 190,
            "y": 592
        }, "City/State/Zip": {
            "x": 190,
            "y": 578
        }, "SID#": {
            "x": 190,
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
            "x": 490,
            "y": 682
        },
        "BarCode": {
            "x": 490,
            "y": 682
        }
    },
    "CarrierDetails": {

        "CarrierName": {
            "x": 485,
            "y": 617
        },
        "TrailerNo": {
            "x": 485,
            "y": 605
        },
        "SealNo": {
            "x": 485,
            "y": 593
        },
        "SCAC": {
            "x": 485,
            "y": 575
        },
        "PRO": {
            "x": 485,
            "y": 565
        },
        "PROBarCode": {
            "x": 485,
            "y": 545
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
                "xY": 352.5,
                "xN": 388.5,
                "dx": 0.5, 
                "dy": 1
            },
        },
        "rows": [
            418,
            400,
            382,
            364,
            653,
            635,
            617,
            599,
            581,
            563,
            545,
            527,
            509,
            491,
            473,
            455,
            437,
            419,
            401,
            383,
            365,
            347,
            329,
            311,
            293,
            275,
            257,
            239,


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
                "x": 55,
                "dy": 4
            },
            "HUType": {
                "x": 90,
                "dy": 4
            },
            "PkgQty": {
                "x": 127,
                "dy": 4
            },
            "PkgType": {
                "x": 163,
                "dy": 4
            },
            "Weight": {
                "x": 210,
                "dy": 4
            },
            "HM": {
                "x": 254,
                "dy": 4
            },
            "Desc": {
                "x": 380,
                "dy": 4
            },
            "NMFC": {
                "x": 510,
                "dy": 4
            },
            "Class": {
                "x": 555,
                "dy": 4
            },
        },
        "rows": [
            282,
            264,
            246,
            228,
            210,
            318,
            300,
            282,
            264,
            246,
            228,
            210,
            192,
            174,
            156,      

        ]
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
     canvas.drawString(x-(width/2), y, text)

pkey_types1 = ["ShipFrom", "ShipTo", "ThirdParty", "BOL", "CarrierDetails", "Footer"]

def generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)

    data = json.loads(json_data)

    packet_1 = io.BytesIO()
    packet_2 = io.BytesIO()
    first_pdf_canvas = canvas.Canvas(packet_1, pagesize=letter)
    second_pdf_canvas = canvas.Canvas(packet_2, pagesize=letter)
    # page 1
    for pk in data:
        if pk in pkey_types1:
            for key in data[pk]:
                x = position_dict[pk][key]["x"]
                y = position_dict[pk][key]["y"]
                first_pdf_canvas.setFont("Helvetica", 8)
                second_pdf_canvas.setFont("Helvetica", 8)
                text_center_draw(first_pdf_canvas, x, y, data[pk][key], "Helvetica", 8)
        elif pk == "OrderInfo":
            idx = 0
            for row_data in data[pk]['Items']:
                for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                    val = row_data[key]
                    if idx < 4:
                        
                        dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                        y = position_dict["OrderInfo"]["rows"][idx]
                        # print(x, y, dy)
                        if val == "N":
                            x = position_dict["OrderInfo"]["page_one_column"][key]["xN"]
                            val = "O"
                        elif val == "Y":
                            x = position_dict["OrderInfo"]["page_one_column"][key]["xY"]
                            val = "O"
                        else:
                            x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                        text_center_draw(first_pdf_canvas, x, y + dy, val, "Helvetica", 8)
                    elif idx < 19:
                        dx = position_dict["OrderInfo"]["page_one_column"][key]["dx"]
                        dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                        y = position_dict["OrderInfo"]["rows"][idx]
                        if val == "N":
                            x = position_dict["OrderInfo"]["page_one_column"][key]["xN"]
                            val = "O"
                        elif val == "Y":
                            x = position_dict["OrderInfo"]["page_one_column"][key]["xY"]
                            val = "O"
                        else:
                            x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                        text_center_draw(second_pdf_canvas, x - dx, y + dy, val, "Helvetica", 8)
                        
                idx += 1
        elif pk == "CarrierInfo":
            idx = 0
            for row_data in data[pk]['Items']:
                for key in ["HUQty", "HUType", "PkgQty", "PkgType", "Weight", "HM", "Desc", "NMFC", "Class"]:
                    val = row_data[key]
                    if idx < 5:
                        x = position_dict[pk]["page_one_column"][key]["x"]
                        dy = position_dict[pk]["page_one_column"][key]["dy"]
                        y = position_dict[pk]["rows"][idx]
                        text_center_draw(first_pdf_canvas, x, y + dy, val, "Helvetica", 8)
                    elif idx < 11:
                        x = position_dict[pk]["page_one_column"][key]["x"]
                        dy = position_dict[pk]["page_two_column"][key]["dy"]
                        y = position_dict[pk]["rows"][idx]

                        text_center_draw(second_pdf_canvas, x, y + dy, val, "Helvetica", 8)
                idx += 1

    # page1
    first_pdf_canvas.showPage()
    # page2
    second_pdf_canvas.showPage()
    
    first_pdf_canvas.save()
    second_pdf_canvas.save()

    packet_1.seek(0)
    packet_2.seek(0)

    first_page_pdf = PdfReader(packet_1)
    second_page_pdf = PdfReader(packet_2)


    existing_pdf = PdfReader(open("vics-stand.pdf", "rb"))
    output = PdfWriter()
    first_page = existing_pdf.pages[0]
    first_page.merge_page(first_page_pdf.pages[0])

    second_Page = existing_pdf.pages[1]
    second_Page.merge_page(second_page_pdf.pages[0])
    output.add_page(first_page)
    output.add_page(second_Page)
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()
