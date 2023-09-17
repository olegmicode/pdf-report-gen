from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Vera',normal='Vera',bold='',italic='VeraIt',boldItalic='VeraBI')
import json

# with open("data.json") as file:
#     data = json.load(file)

# # print(data)

# json_data = json.dumps(data)

# data = f"""{json_data}"""
# ship_from = data['ShipFrom']['name']

# json_name = json.loads(ship_from)
# name = json_name("Name")
# Extract the "Name" value from "ShipFrom"
# ##########################
# ship_from_name = json.loads(json_data)['ShipFrom']['Name']

# # Extract the "Name" value from "ShipTo"
# ship_to_name = json.loads(json_data)['ShipTo']['Name']

# # Name, Address, City_State_Zip, SID, FOB =
# # Print the extracted values
# print("Ship From Name:", ship_from_name)
# print("Ship To Name:", ship_to_name)
# #################################

# data = json.loads(json_data)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 10, "addr")
can.setFont("DarkGardenMK", 33)

for i in range(0, 2000, 15):
    print(i)
    can.line(0, i, 1300, i)
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open("vics-stand.pdf", "rb"))
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
nextPage = existing_pdf.pages[1]
output.add_page(page)
output.add_page(nextPage)
# finally, write "output" to a real file
output_stream = open("destination.pdf", "wb")
output.write(output_stream)
output_stream.close()