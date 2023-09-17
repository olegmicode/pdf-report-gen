from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Vera',normal='Vera',bold='',italic='VeraIt',boldItalic='VeraBI')
import json

with open("data.json") as file:
    data = json.load(file)

# print(data)

json_data = json.dumps(data)

# data = f"""{json_data}"""
# ship_from = data['ShipFrom']['name']

# json_name = json.loads(ship_from)
# name = json_name("Name")
# Extract the "Name" value from "ShipFrom"
##########################
# ship_from_name = json.loads(json_data)['ShipFrom']['Name']

# # Extract the "Name" value from "ShipTo"
# ship_to_name = json.loads(json_data)['ShipTo']['Name']

# # Name, Address, City_State_Zip, SID, FOB =
# # Print the extracted values
# print("Ship From Name:", ship_from_name)
# print("Ship To Name:", ship_to_name)
# #################################

data = json.loads(json_data)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
for key1 in  data:
    if key1 == "ShipFrom":
        x = 150
        y = 678
        for key2 in data[key1]:
            can.setFont("Helvetica", 8)
            can.drawString(x, y, data[key1][key2])
            y -= 14
    if key1 == "ShipTo":
        x = 150
        y = 606
        for key2 in data[key1]:
            can.setFont("Helvetica", 8)
            can.drawString(x, y, data[key1][key2])
            y -= 14
    if key1 == "ThirdParty":
        x = 150
        y = 533
        for key2 in data[key1]:
            can.setFont("Helvetica", 8)
            if(key2 == "SpecialInstructions"):
                can.drawString(x, y - 3 , data[key1][key2])
            else:
                can.drawString(x, y, data[key1][key2])
                y -= 14
    if key1 == "BOL":
        x = 450
        y = 682
        for key2 in data[key1]:
            can.drawString(x, y, data[key1][key2])
            x = 430
            y = 655
    if key1 == "CarrierDetails":
        x = 450
        y = 617
        for key2 in data[key1]:
            if(key2 == "SCAC"):
                can.drawString(x, 575, data[key1][key2])
            elif(key2 == "PRO"):
                can.drawString(x, 565, data[key1][key2])
            elif(key2 == "PROBarCode"):
                can.drawString(x, 545, data[key1][key2])
            elif(key2 == "Prepaid"):
                can.drawString(388, 487, data[key1][key2])
            elif(key2 == "Collect"):
                can.drawString(460, 487, data[key1][key2])
            elif(key2 == "3rdParty"):
                can.drawString(538, 487, data[key1][key2])
            elif(key2 == "MasterBOL"):
                can.drawString(378, 471, data[key1][key2])
            else:
                can.drawString(x, y, data[key1][key2])
                y -= 12
    if key1 == "OrderInfo":
        x = 105
        y = 418
        cnt = 0 
        for key2 in data[key1]:    
            for idx in data[key1][key2]:
                cnt += 1               
                can.drawString(x, y, idx["OrderNo"])
                can.drawString(x + 120, y,  idx["Pkgs"])
                can.drawString(x + 182, y,  idx["Weight"])
                can.drawString(x + 320, y,  idx["AddInfo"])
                can.drawString(x + 281, y+1,  idx["PalletSlip"])
                y -= 18
                print(cnt)
                if cnt > 4:
                    


# can.drawString(10, 10, "addr")
# can.setFont("DarkGardenMK", 33)
can.save()

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