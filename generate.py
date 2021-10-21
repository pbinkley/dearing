from fpdf import FPDF
import json

data = json.load(open('testdata.json'))

pdf = FPDF(orientation = 'L', unit = 'in', format = (3, 5))
pdf.add_page()
pdf.set_font('Courier', 'B', 12)
pdf.set_text_color(0, 0, 0)
pdf.set_margin(0)

x = 2.5
y = 1
w = 1
h = 1
txt = 'O'
border = 0
align = 2
fill = False

fields = data["fieldlist"]

y = 0.25
w = 0.125
h = 0.125

count = len(fields)

space = 5 / (count + 1)
firstcard = True

for group in data["groups"]:
    for card in group["cards"]:
        if not firstcard:
            pdf.add_page()
        firstcard = False

        # one card for each card
        pos = 1
        for field in fields:
            x = pos * space - w/2
            pdf.set_draw_color(r=0, g=0, b=0)
            pdf.set_fill_color(255)

            # draw notch if this field is in this card.fields
            if field in card['fields']:
                pdf.line(x1=x-w, y1=0, x2=x, y2=y+0.125)
                pdf.line(x1=x+w, y1=0, x2=x, y2=y+0.125)

            # draw circle for hole
            pdf.ellipse(x=x - w/2, y=y, w=w, h=h, style="FD")

            # add field label below circle
            pdf.set_xy(x - w/2, y * 2)
            pdf.cell(w, h, fields[pos-1], border, align='C')

            pos += 1

        pdf.set_xy(1,1)
        pdf.cell(3, 0.5, data["grouplabel"] +": " + group["id"])
        pdf.set_xy(1,1.25)
        pdf.cell(3, 0.5, data["cardlabel"] + ": " + card["text"])

        pdf.set_xy(0.25,2.5)
        pdf.cell(3, 0.25, "Source: " + data["label"])

pdf.output('test.pdf', 'F')
