# Array
page_params = {
    "marginLeft": 15,  # margin left on real page's canvas
    "marginRight": 15,  # margin rigth on real page's canvas
    "marginTop": 18,  # margin top on real page's canvas
    "marginBottom": 12,  # margin bottom on real page's canvas
    "paperWidth": 574,  # width for real page's canvas
    "paperHeight": 640,  # height for real page's canvas
    "width": 100,  # virtual width for draw
    "height": 100,  # virtual height for draw
}

data_pos = {
    "BlanketPeriod": {
        "DateFrom": {
            "x": 4,
            "y": 2.55,
        },
        "DateTo": {
            "x": 14.44,
            "y": 2.55,
        }
    },
    "SingleShipment": {
        "x": 64,
        "y": 1.05,
        "w": 0,
        "h": 0
    },
    "ReferenceNumber": {
        "x": 64,
        "y": 2.55,
        "w": 0,
        "h": 0
    },
    "CertifyingParty": {
        "x": 0,
        "y": 0,
        "w": 0,
        "h": 0
    },
    "Certifier": {
        "CompanyName": {
            "x": 0.5,
            "y": 7,
        },
        "Phone": {
            "x": 6.2,
            "y": 15.45,
        },
        "Email": {
            "x": 8.5,
            "y": 18.25,
        },
        "Address": {
            "x": 0.5,
            "y": 8.5,
        },
        "City": {
            "x": 0.5,
            "y": 10,
        },
        "PostalCode": {
            "x": 0.5,
            "y": 11.5,
        },
        "TaxID": {
            "x": 22,
            "y": 15.45,
        }
    },
    "Exporter": {
        "CompanyName": {
            "x": 50.5,
            "y": 7,
        },
        "Phone": {
            "x": 56.2,
            "y": 18.55,
        },
        "Email": {
            "x": 58.5,
            "y": 21.35,
        },
        "Address": {
            "x": 50.5,
            "y": 8.5,
        },
        "City": {
            "x": 50.5,
            "y": 10,
        },
        "PostalCode": {
            "x": 50.5,
            "y": 11.5,
        },
        "TaxID": {
            "x": 72,
            "y": 18.55,
        }
    },
    "Producer": {
        "CompanyName": {
            "x": 0.5,
            "y": 26,
        },
        "Phone": {
            "x": 6.2,
            "y": 35.95,
        },
        "Email": {
            "x": 8.5,
            "y": 38.75,
        },
        "Address": {
            "x": 0.5,
            "y": 27.5,
        },
        "City": {
            "x": 0.5,
            "y": 29,
        },
        "PostalCode": {
            "x": 0.5,
            "y": 30.5,
        },
        "TaxID": {
            "x": 22,
            "y": 35.95,
        }
    },
    "Importer": {
        "CompanyName": {
            "x": 50.5,
            "y": 26,
        },
        "Phone": {
            "x": 56.2,
            "y": 35.95,
        },
        "Email": {
            "x": 58.5,
            "y": 38.75,
        },
        "Address": {
            "x": 50.5,
            "y": 27.5,
        },
        "City": {
            "x": 50.5,
            "y": 29,
        },
        "PostalCode": {
            "x": 50.5,
            "y": 30.5,
        },
        "TaxID": {
            "x": 72,
            "y": 35.95,
        }
    },
    "LineItems": {
        "PartNumber": {
            "x": 0,
            "y": 0,
        },
        "Description": {
            "x": 0,
            "y": 0,
        },
        "HSTariffClarification": {
            "x": 0,
            "y": 0,
        },
        "OriginCriterion": {
            "x": 0,
            "y": 0,
        },
        "CountryOfOrigin": {
            "x": 0,
            "y": 0,
        },
    },
    "Signatory": {
        "Name": {
            "x": 0.5,
            "y": 93,
        },
        "CompanyName": {
            "x": 50.5,
            "y": 88,
        },
        "Title": {
            "x": 50.5,
            "y": 93,
        },
        "Email": {
            "x": 20.25,
            "y": 97.8,
        },
        "Phone": {
            "x": 50.5,
            "y": 97.8,
        },
        "Date": {
            "x": 0.5,
            "y": 97.8,
        },
    }

}


def text_center_draw(canvas, x, y, text, font, size, dy=0, align="center"):
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
