# Array
from reportlab.pdfgen import canvas
page_params = {
    "marginLeft": 45,  # margin left on real page's canvas
    "marginRight": 5,  # margin rigth on real page's canvas
    "marginTop": -126,  # margin top on real page's canvas
    "marginBottom": 50,  # margin bottom on real page's canvas
    "paperWidth": 560,  # width for real page's canvas
    "paperHeight": 600,  # height for real page's canvas
    "width": 100,  # virtual width for draw
    "height": 100,  # virtual height for draw
}

data_pos = {
    "AirWaybillNumber": {
        "x": 65,
        "y": 1.5
    },
    "ShipperReferenceNumber": {
        "x": 78,
        "y": 6
    },
    "Pages": {
        "x": 56.25,
        "y": 4.1,
        "w": 3
    },
    "ShipFrom": {
        "CompanyName": {
            "x": 1,
            "y": 3
        },
        "Address": {
            "x": 1,
            "y": 5
        },
        "City": {
            "x": 1,
            "y": 6.5
        },
        "PostalCode": {
            "x": 1,
            "y": 8
        }
    },
    "ShipTo": {
        "Name": {
            "x": 1,
            "y": 12
        },
        "Address": {
            "x": 1,
            "y": 14
        },
        "City": {
            "x": 1,
            "y": 15.5
        },

        "PostalCode": {
            "x": 1,
            "y": 17
        },

    },
    "TransportDetails": {
        "AirService": {
            "x": 0,
            "y": 0
        },
        "AirportOfDeparture": {
            "x": 0,
            "y": 0
        },
        "AirportOfDestination": {
            "x": 0,
            "y": 0
        }
    },
    "ShipmentType": {
        "RadioActive": {
            "x": 0,
            "y": 0
        }
    },
    "DangerousGoods": [
        {
            "ActualQuantity": {
                "x": 0,
                "y": 0
            },
            "PackingType": {
                "x": 0,
                "y": 0
            },
            "UNNumber": {
                "x": 0,
                "y": 0
            },
            "ProperShippingName": {
                "x": 0,
                "y": 0
            },
            "TechnicalName": {
                "x": 0,
                "y": 0
            },
            "HazmatClass": {
                "x": 0,
                "y": 0
            },
            "PackingGroup": {
                "x": 0,
                "y": 0
            },
            "ActualUOM": {
                "x": 0,
                "y": 0
            },
            "PackingInstructions": {
                "x": 0,
                "y": 0
            },
            "ShipType": {
                "x": 0,
                "y": 0
            }
        }
    ],
    "AdditionalHandlingInformation": {
        "EmergencyContact": {
            "x": 0,
            "y": 0
        },
        "EmergengyContactNo": {
            "x": 0,
            "y": 0
        },
        "ShipperName": {
            "x": 0,
            "y": 0
        },
        "ShipmentDate": {
            "x": 0,
            "y": 0
        }
    }
}


first_page_count = 11
page_item_count = 31


def text_draw_on_canvas(canvas, x, y, text, font, size, dy=0, align="center"):
    if align == "center":
        width = canvas.stringWidth(text=text, fontName=font, fontSize=size)
        canvas.setFont(font, size)
        canvas.drawString(x-(width/2), y + dy, text)
    elif align == "left":
        width = canvas.stringWidth(text=text, fontName=font, fontSize=size)
        canvas.setFont(font, size)
        canvas.drawString(x, y + dy, text)


def translate_positon_to_pdf(x, y, w=0, h=0):
    margin_left = page_params['marginLeft']
    margin_right = page_params['marginRight']
    margin_top = page_params['marginTop']
    margin_bottom = page_params['marginBottom']
    paper_width = page_params['paperWidth']
    paper_height = page_params['paperHeight']
    content_width = paper_width - margin_left - margin_right
    content_height = paper_height - margin_top - margin_bottom

    max_width = page_params['width']
    max_height = page_params['height']

    r_x = x / max_width * content_width + margin_left
    r_y = (max_height - y) / max_height * \
        content_height + margin_bottom
    r_w = w / max_width * content_width
    r_h = h / max_height * content_height

    return [r_x, r_y, r_w, r_h]


def draw_multiline_string(canvas, text, x, y, width, line_height):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if canvas.stringWidth(current_line + ' ' + word) < width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    for line in lines:
        canvas.drawString(x, y, line)
        y -= line_height
