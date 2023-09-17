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
            "y": 533
        },
        "City/State/Zip": {
            "x": 150,
            "y": 533
        },
        "SpecialInstructions": {
            "x": 150,
            "y": 533
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
            "y": 617
        },
        "SealNo": {
            "x": 450,
            "y": 617
        },
        "SCAC": {
            "x": 450,
            "y": 617
        },
        "PRO": {
            "x": 450,
            "y": 617
        },
        "PROBarCode": {
            "x": 450,
            "y": 617
        },
        "Prepaid": {
            "x": 450,
            "y": 617
        },
        "Collect": {
            "x": 450,
            "y": 617
        },
        "3rdParty": {
            "x": 450,
            "y": 617
        },
        "MasterBOL": {
            "x": 450,
            "y": 617
        },

    },
    "OrderInfo": {
        "column1": {
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
            481,
            463,
            445,
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
}


def generate_pdf_from_json(json_file_path, output_pdf_path):
    with open(json_file_path) as file:
        data = json.load(file)

    json_data = json.dumps(data)

    data = json.loads(json_data)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    for pk in data:
        if pk == "ShipFrom" or pk == "ShipTo" or pk == "ThirdParty" or pk == "BOL":
            for key in data[pk]:
                x = position_dict[pk][key]
                can.drawString(x, y, data[pk][key])

        if pk == "CarrierDetails":
            x = 450
            y = 617
            for key in data[pk]:
                if (key == "SCAC"):
                    can.drawString(x, 575, data[pk][key])
                elif (key == "PRO"):
                    can.drawString(x, 565, data[pk][key])
                elif (key == "PROBarCode"):
                    can.drawString(x, 545, data[pk][key])
                elif (key == "Prepaid"):
                    can.drawString(388, 487, data[pk][key])
                elif (key == "Collect"):
                    can.drawString(460, 487, data[pk][key])
                elif (key == "3rdParty"):
                    can.drawString(538, 487, data[pk][key])
                elif (key == "MasterBOL"):
                    can.drawString(378, 471, data[pk][key])
                else:
                    can.drawString(x, y, data[pk][key])
                    y -= 12
        if pk == "OrderInfo":
            x = 105
            y = 418
            cnt = 0
            for key in data[pk]:
                for idx in data[pk][key]:
                    cnt += 1
                    can.drawString(x, y, idx["OrderNo"])
                    can.drawString(x + 120, y,  idx["Pkgs"])
                    can.drawString(x + 182, y,  idx["Weight"])
                    can.drawString(x + 320, y,  idx["AddInfo"])
                    can.drawString(x + 281, y+1,  idx["PalletSlip"])
                    y -= 18
                    print(cnt)
                    if cnt > 4:
                        break

    can.save()

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
