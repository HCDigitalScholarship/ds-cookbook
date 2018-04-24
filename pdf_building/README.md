## Dynamically creating PDFs with reportlab

reportlab is a software for building PDFs from XML or Python instructions. Because it can interpret Python instructions, reportlab can be used to dynamically generate PDFs that vary in format and content. For instance, if we want to give site visitors the ability to view and download digitized resources as a PDF rather than a webpage, reportlab can be used in the backend to fill out a PDF template with the relevant content and metadata, or even make structural changes to a PDF document according to user specifications, database content, or other parameters.

### Basics

reportlab can be installed with pip:

`pip install reportlab`

The basic import from the reportlab module is called `canvas`, the module containing the object class which represents your in-progress PDF.

`from reportlab.pdfgen import canvas`

To begin creating a PDF, initialize a `Canvas` object, passing it the filename where you want it to write to:

`c = canvas.Canvas("something.pdf")`

To write text to your canvas:

`c.drawString(100,750,"These are some words!")`

The first two arguments are the x and y coordinates of the bottom left of the text. All coordinates in reportlab specify the bottom left corner of an object relative to the bottom left of the page, with positive coordinates moving to the right and up.

And to save it to the specified file:

`c.save()`

### Units

Pretty quickly, it will become handy to import a few more things. For instance, dimensions and locations are by default specified in pixels, but it might be easier to work with standard layouts and units. `reportlab.lib` contains units like inches and centimeters which are just numbers of pixels, and some standard page dimensions which are just tuples:

```
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter # 8.5 x 11 inches

c = canvas.Canvas("something.pdf", pagesize=letter)
width, height = letter
c.drawString(1*inch, 2*inch, "These are some words!")
c.save()
```

### Fonts

To specify font, you have to call `setFont` which will dictate the font and font size used until the next time it gets called.

```
c.setFont('Helvetica', 12)
c.drawString(1*inch, 3*inch, "These are some words!") # in Helvetica
c.setFont('Times-Roman', 12)
c.drawString(1*inch, 2*inch, "These are some F A N C Y words!") # in Times New Roman
```

To use a non-standard font from a TrueType file, you'll need to register it like so:

```
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Georgia','/var/www/html/static/fonts/georgia.ttf'))

c.setFont('Georgia', 12)
c.drawString(1*inch, 3*inch, "These are some words!") # in Georgia
```

### Paragraphs

The `drawString` method can only write text in a single line. If you try to write too much text in one `drawString` call, it'll simply run off the edge of the page, and a Python `'\n'` newline character will just render as a black square. If you want to write a paragraph, reportlab's built-in text objects provide basic functionality like a virtual cursor that can be progressively moved down the page:

```
paragraph = c.beginText()
paragraph.setTextOrigin(inch, 8*inch)
paragraph.setFont("Helvetica", 12)
  
for line in lines:
    paragraph.textOut(line)
    paragraph.moveCursor(0,18) # moves the cursor so the next line begins 18 pixels below

c.drawText(paragraph)
```

Unlike normal, moving the cursor in a positive y direction is always downward.

Unfortunately this still requires that you break the text into lines yourself. This helper function I wrote for the Ticha PDF builder may be of use:

```
''' breaks a string into lines of a maximum width, without separating words across a line break '''
def break_by_width(s,width):
    lines = [s.split(' ')]
    i=0
    while i<len(lines):
        for j in range(len(lines[i])):
            if len(' '.join(lines[i][:j])) > width:
                lines.append(lines[i][j-1:])
                lines[i] = lines[i][:j-1]
        i += 1
    return [' '.join(line) for line in lines]
```

### Page Breaks

To move onto a new page, call

`c.showPage()`

Much like with line breaks, handling the logic of when to create a page break is up to you. After calling `showPage()`, you have to `setFont` again even if you want it to stay the same.

### Images

Drawing images on the canvas is fairly straightforward:

`c.drawImage('/var/www/html/static/img/ticha1.gif', 3.75*inch, 9.4*inch, inch, .6*inch)`

Here, the first two coordinates are the x and y of the image's bottom left corner and the next two are its width and height.

If you want to load an image from a PIL Image object rather than a file, you'll need to import the ImageReader module.

```
from reportlab.lib.utils import ImageReader
from PIL import Image

image = Image.open('/var/www/html/static/img/ticha1.gif')
c.drawImage(ImageReader(image), 3.75*inch, 9.4*inch, inch, .6*inch)
```

### More

You can find fuller documentation [here](https://www.reportlab.com/docs/reportlab-userguide.pdf).

For examples of implementation of columns, page numbers, and watermarks, take a look at the Ticha pdf builder.