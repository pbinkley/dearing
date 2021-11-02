from fpdf import FPDF
import json

stockformats = {
    'card': {
        'format': (3,5),
        'locations': [(0,0)]
    },
    'avery': {
        'format': (11,8.5),
        # TODO: confirm these placements of the three cards on an Avery sheet
        'locations': [(1,1.75), (4,1.75), (7,1.75)]
    }
}

# the output format is assumed to be a 3x5 card for now

data = json.load(open('testdata.json'))
format = 'avery'
stockformat = stockformats[format]

location = stockformat['locations'][2]

pdf = FPDF(orientation = 'L', unit = 'in', format = stockformats[format]['format'])
pdf.add_page()
pdf.set_font('Courier', 'B', 12)
pdf.set_text_color(0, 0, 0)
pdf.set_margin(0)

txt = 'O'
border = 0
align = 2
fill = False

fields = data["fieldlist"]

hole_height = 0.25
hole_width = 0.125
h = 0.125

count = len(fields)

space = 5 / (count + 1)
newpage = True

for group in data["groups"]:
    for card in group["cards"]:
        if not newpage:
            pdf.add_page()
        newpage = False

        xoffset = location[1]
        yoffset = location[0]

        # one card for each card
        pos = 1
        for field in fields:
            x = xoffset + pos * space - hole_width/2
            pdf.set_draw_color(r=0, g=0, b=0)
            pdf.set_fill_color(255)

            # draw notch if this field is in this card.fields
            if field in card['fields']:
                pdf.line(x1=x-(hole_width/2), y1=yoffset, x2=x, y2=0.25+hole_width/2 + yoffset)
                pdf.line(x1=x+(hole_width/2), y1=yoffset, x2=x, y2=0.25+hole_width/2+yoffset)

            # draw circle for hole
            pdf.ellipse(x=x - hole_width/2, y=yoffset+0.1875, w=hole_width, h=hole_width, style="FD")

            # add field label below circle
            pdf.set_xy(x - hole_width/2, 2*hole_height - 0.125 + yoffset)
            pdf.cell(hole_width, h, fields[pos-1], border, align='C')

            pos += 1

        # reset position
        pdf.set_xy(0,0)

        pdf.set_xy(xoffset + 1, yoffset +1)
        pdf.cell(3, 0.5, data["grouplabel"] +": " + group["id"])
        pdf.set_xy(xoffset + 1,yoffset + 1.25)
        pdf.cell(3, 0.5, data["cardlabel"] + ": " + card["text"])

        pdf.set_xy(xoffset + 0.25,yoffset + 2.5)
        pdf.cell(3, 0.25, "Source: " + data["label"])

        # draw card outline
        # TODO: make optional
        pdf.rect(x=xoffset, y=yoffset, w=5, h=3, style='D')

        # TODO: add corner cut at lower right

pdf.output('test.pdf', 'F')
