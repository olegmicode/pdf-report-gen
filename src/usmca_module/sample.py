import pandas as pd


def first_page_total_Cal(pdf_canvas, data, sub_total):
    Total_Pkgs = 0  # len(data["items"])
    Total_No_unit = 0
    Total_netWeight = 0
    invoice_total = 0
    # draw page_number
    text_center_draw(pdf_canvas, 560, 703, "1", "Helvetica", 7)

    df = pd.DataFrame(data["items"])
    df[['quantity', 'uom']] = df["quantity"].str.split(expand=True)
    df['quantity'] = pd.to_numeric(df['quantity'])
    Total_No_unit = df["quantity"].sum()

    df['num_packages'] = pd.to_numeric(df['num_packages'])
    Total_Pkgs = df["num_packages"].sum()

    df['net_weight'] = pd.to_numeric(df['net_weight'])
    Total_netWeight = df["net_weight"].sum()

    df['value'] = pd.to_numeric(df['value'])
    invoice_total = df["value"].sum()

    # for item in data["items"]:
    # for key in item:
    # if key == "quantity":
    # strVal = item[key]
    # val = strVal.split(" ")
    # Total_No_unit += float(val[0])
    # elif key == "net_weight":
    # Total_netWeight += float(item["net_weight"])
    # elif key == "value":
    # invoice_total += float(item["value"])
    # elif key == "num_packages":
    # Total_Pkgs += float(item["num_packages"])
    y = position_dict["first_page_total"]["y"]
    # N of Pkgs
    x = position_dict["items"]["item_field"]["num_packages"]["x"]
    text_center_draw(pdf_canvas, x, y, Total_Pkgs, "Helvetica", 6)
    # quantity
    x = position_dict["items"]["item_field"]["quantity"]["x1"]
    text_center_draw(pdf_canvas, x, y, Total_No_unit, "Helvetica", 6)

    # Net weight
    x = position_dict["items"]["item_field"]["net_weight"]["x"]
    text_center_draw(pdf_canvas, x + 10, y,
                     str(Total_netWeight) + " LBS", "Helvetica", 6)
    # sub total
    x = position_dict["totals"]["subTotal"]["x"]
    y = position_dict["totals"]["subTotal"]["y"]
    text_center_draw(pdf_canvas, x, y, sub_total, "Helvetica", 6)
    # invoice total
    x = position_dict["totals"]["Invoice_Total"]["x"]
    y = position_dict["totals"]["Invoice_Total"]["y"]
    text_center_draw(pdf_canvas, x, y, invoice_total, "Helvetica", 6)

    for pk in data:
        if pk == "totals":
            for key in data[pk]:
                y = position_dict["totals"][key]["y"]
                text_center_draw(pdf_canvas, x, y,
                                 data[pk][key], "Helvetica", 6)
                x = position_dict["totals"][key]["x"]
