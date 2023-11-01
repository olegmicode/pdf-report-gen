# Array
from reportlab.pdfgen import canvas
page_params = {
    "marginLeft": 25,  # margin left on real page's canvas
    "marginRight": 25,  # margin rigth on real page's canvas
    "marginTop": 40,  # margin top on real page's canvas
    "marginBottom": 30,  # margin bottom on real page's canvas
    "paperWidth": 610,  # width for real page's canvas
    "paperHeight": 800,  # height for real page's canvas
    "width": 100,  # virtual width for draw
    "height": 100,  # virtual height for draw
}

data_pos = {
    "AccountNumber": {
        "x": 1,
        "y": 1.5
    },
    "EmergencyContactNumber": {
        "x": 16,
        "y": 1.5
    },
    "ShipperName": {
        "x": 26,
        "y": 1.5
    },
    "TrackingNumber": {
        "x": 1,
        "y": 4
    },
    "HazardousMaterials": {
        "x": 1,
        "y": 6.5,
        "dy": 2
    },
    "SignatoryName": {
        "x": 3,
        "y": 21
    },
    "ShipmentDate": {
        "x": 35,
        "y": 21
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
