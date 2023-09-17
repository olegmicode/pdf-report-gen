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
            "x": 150,
            "y": 678
        },
        "Address": {
            "x": 150,
            "y": 664
        },
        "City/State/Zip": {
            "x": 150,
            "y": 650
        },
        "SID#": {
            "x": 150,
            "y": 636
        },
        "FOB": {
            "x": 150,
            "y": 622
        }
    },
    "ShipTo": {

        "Name": {
            "x": 150,
            "y": 606
        }, "Address": {
            "x": 150,
            "y": 592
        }, "City/State/Zip": {
            "x": 150,
            "y": 578
        }, "SID#": {
            "x": 150,
            "y": 564
        }, "FOB": {
            "x": 150,
            "y": 550
        }
    },
    "ThirdParty": {

        "Name": {
            "x": 150,
            "y": 533
        },
        "Address": {
            "x": 150,
            "y": 519
        },
        "City/State/Zip": {
            "x": 150,
            "y": 505
        },
        "SpecialInstructions": {
            "x": 150,
            "y": 487
        },
    },
    "BOL": {
        "BOLNumber": {
            "x": 450,
            "y": 682
        },
        "BarCode": {
            "x": 450,
            "y": 682
        }
    },
    "CarrierDetails": {

        "CarrierName": {
            "x": 450,
            "y": 617
        },
        "TrailerNo": {
            "x": 450,
            "y": 605
        },
        "SealNo": {
            "x": 450,
            "y": 593
        },
        "SCAC": {
            "x": 450,
            "y": 575
        },
        "PRO": {
            "x": 450,
            "y": 565
        },
        "PROBarCode": {
            "x": 450,
            "y": 545
        },
        "Prepaid": {
            "x": 388,
            "y": 487
        },
        "Collect": {
            "x": 460,
            "y": 487
        },
        "3rdParty": {
            "x": 450,
            "y": 617
        },
        "MasterBOL": {
            "x": 378,
            "y": 471
        },

    },
    "OrderInfo": {
        "page_one_column": {
            "OrderNo": {
                "x": 105,
                "dy": 0
            },
            "Pkgs": {
                "x": 225,
                "dy": 0
            },
            "Weight": {
                "x": 285,
                "dy": 0
            },
            "AddInfo": {
                "x": 425,
                "dy": 0
            },
            "PalletSlip": {
                "x": 396,
                "dy": 1
            },
        },
        "page_two_column": {
            "OrderNo": {
                "x": 105,
                "dy": 0
            },
            "Pkgs": {
                "x": 225,
                "dy": 0
            },
            "Weight": {
                "x": 285,
                "dy": 0
            },
            "AddInfo": {
                "x": 425,
                "dy": 0
            },
            "PalletSlip": {
                "x": 396,
                "dy": 1
            },
        },
        "rows": [
            418,
            400,
            382,
            364,
            427,
            409,
            391,
            373,
            355,
            337,
            319,
            301,
            283,
            265,
            247,
            229,
            211,
            193,
            175,
            157,
            139,
            121,
            103,
            85,
            67,
            49,
            31,
            13,


        ]
    },
    "CarrierInfo": {
        "page_one_column": {
            "HUQty": {
                "x": 52,
                "dy": 0
            },
            "HUType": {
                "x": 80,
                "dy": 0
            },
            "PkgQty": {
                "x": 108,
                "dy": 0
            },
            "PkgType": {
                "x": 136,
                "dy": 0
            },
            "Weight": {
                "x": 396,
                "dy": 1
            },
            "HM": {
                "x": 396,
                "dy": 1
            },
            "Desc": {
                "x": 396,
                "dy": 1
            },
            "NMFC": {
                "x": 396,
                "dy": 1
            },
            "Class": {
                "x": 396,
                "dy": 1
            },
        },
        "rows": [
            282,
            264,
            246,
            228,
            210,
            192,
            174,
            355,
            337,
            319,
            301,
            283,
            265,
            247,
            229,
            211,
            193,
            175,
            157,
            139,
            121,
            103,
            85,
            67,
            49,
            31,
            13,


        ]
    },
}
pkey_types1 = ["ShipFrom", "ShipTo", "ThirdParty", "BOL", "CarrierDetails"]


def generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)

    data = json.loads(json_data)

    packet = io.BytesIO()
    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    # page 1
    for pk in data:
        if pk in pkey_types1:
            for key in data[pk]:
                x = position_dict[pk][key]["x"]
                y = position_dict[pk][key]["y"]
                pdf_canvas.setFont("Helvetica", 8)
                pdf_canvas.drawString(x, y, data[pk][key])
        elif pk == "OrderInfo":
            idx = 0
            for row_data in data[pk]['Items']:
                for key in ["OrderNo", "Pkgs", "Weight", "AddInfo", "PalletSlip"]:
                    val = row_data[key]
                    if idx < 4:
                        x = position_dict["OrderInfo"]["page_one_column"][key]["x"]
                        dy = position_dict["OrderInfo"]["page_one_column"][key]["dy"]
                        y = position_dict["OrderInfo"]["rows"][idx]
                        print(x, y, dy)
                        pdf_canvas.drawString(x, y + dy, val)
                    # elif idx < 19:
                    #     x = position_dict["OrderInfo"]["page_two_column"][key]["x"]
                    #     dy = position_dict["OrderInfo"]["page_two_column"][key]["dy"]
                    #     y = position_dict["OrderInfo"]["rows"][idx]
                    #     print(x, y, dy)
                    #     can.drawString(x, y + dy, val)
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
                        print(x, y, dy)
                        pdf_canvas.drawString(x, y + dy, val)
                idx += 1

    pdf_canvas.showPage()
    # page2

    pdf_canvas.showPage()
    pdf_canvas.save()

    packet.seek(0)

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open("vics-stand.pdf", "rb"))
    output = PdfWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    nextPage = existing_pdf.pages[1]
    output.add_page(page)
    output.add_page(nextPage)
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()
