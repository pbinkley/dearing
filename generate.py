from fpdf import FPDF
import json
import pdb

stock_formats = {
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

format = 'avery'

stock_format = stock_formats[format]
segment_end = len(stock_format['locations']) # the number of locations, i.e. how many cards per page

card_height = 3
card_width = 5

hole_width = 0.125 
hole_height = 0.25 # height of cell for circle
hole_y = 0.1875 # offset from top of card
label_height = 0.125

data = json.load(open('testdata.json'))
fields = data["fieldlist"] # list of fields, i.e. witnesses
spacing = card_width / (len(fields) + 1) # spacing between holes

# collect cards into single sequence

cards = []

for group in data["groups"]:
    thisgroup = { "group": group["id"] }
    for card in group["cards"]:
        thisgroup["card"] = card
        cards.append(thisgroup.copy())

print("Cards: " + str(len(cards)))

# start PDF

pdf = FPDF(orientation = 'L', unit = 'in', format = stock_format['format'])
pdf.set_font('Courier', 'B', 12)
pdf.set_text_color(0, 0, 0)
pdf.set_margin(0)
pdf.set_draw_color(r=0, g=0, b=0)
pdf.set_fill_color(255)

while len(cards) > 0:

    # capture and delete the cards for this page
    segment = cards[:segment_end]
    del(cards[:segment_end])

    pdf.add_page() # start new page

    card_index = 0
    for item in segment: # card
        location = stock_format['locations'][card_index] # location of this card on page
        card_x = location[1]
        card_y = location[0]

        card_index += 1

        # draw fields (i.e. witnesses) at top of card: holes, notches, labels
        field_index = 1
        for field in fields:
            x = card_x + field_index * spacing - hole_width/2

            # draw notch if this field is in this card.fields
            if field in item['card']['fields']:
                pdf.line(x1=x - hole_width/2, y1=card_y, x2=x, y2=0.25 + hole_width/2 + card_y)
                pdf.line(x1=x + hole_width/2, y1=card_y, x2=x, y2=0.25 + hole_width/2 + card_y)

            # draw circle for hole
            pdf.ellipse(x=x - hole_width/2, y=card_y+hole_y, w=hole_width, h=hole_width, style="FD")

            # add field label below circle
            pdf.set_xy(x - hole_width/2, 2*hole_height - 0.125 + card_y)
            pdf.cell(hole_width, label_height, fields[field_index-1], align='C')

            field_index += 1

        # TODO: make sure long texts are wrapped properly
        # add group id (i.e. id of this variation)
        pdf.set_xy(card_x + 1, card_y + 1)
        pdf.cell(card_height, 0.5, data["grouplabel"] +": " + item["group"])

        # add content (i.e. text of this reading)
        pdf.set_xy(card_x + 1,card_y + 1.25)
        pdf.cell(card_height, 0.5, data["cardlabel"] + ": " + item["card"]["text"])

        # add source (i.e. pack to which this card belongs)
        pdf.set_xy(card_x + 0.25,card_y + 2.5)
        pdf.cell(card_height, 0.25, "Source: " + data["label"])

        # draw card outline, to help with alignment with the form
        # TODO: make optional
        pdf.rect(x=card_x, y=card_y, w=card_width, h=card_height, style='D')

        # TODO: add corner cut at lower right

pdf.output('test.pdf', 'F')
