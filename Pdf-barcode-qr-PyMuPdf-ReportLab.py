import os
import fitz
import qrcode
import barcode
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.barcode import code128, qr
from reportlab.graphics.shapes import Drawing
import config as cfg


# create pdf with pymupdf
f = os.path.join(cfg.LBLPDFt, 'testfz.pdf')
with fitz.open() as doc:
    # create a page with size 800px X 1200px
    pg = doc.new_page(pno=-1, width=800, height=1200)
    # outside border
    pg.draw_line((15, 15), (785, 15), width=3, color=(0, 0, 0, 1))
    pg.draw_line((15, 15), (15, 1185), width=3, color=(0, 0, 0, 1))
    pg.draw_line((15, 1185), (785, 1185), width=3, color=(0, 0, 0, 1))
    pg.draw_line((785, 15), (785, 1185), width=3, color=(0, 0, 0, 1))
    # Settings: font size
    fsz_1 = 24
    fsz_2 = 36
    fsz_3 = 32
    fsz_4 = 42
    fsz_5 = 64
    fsz_6 = 20

    # Qcode
    y = qrcode.QRCode(version=15, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_L)
    y.add_data('http://www.bzking.net')
    y.make(fit=True)
    img = y.make_image(fill='black', back_color='white')
    # temporary image settings
    fnmq = 'SZ405BGP0300050198' + 'q.png'
    fnmq = os.path.join(cfg.LBLPDFt, fnmq)
    img.save(fnmq)
    # add qr code to a specific location on pdf
    pg.insert_image((20, 430, 250, 660), filename=fnmq)
    # remove temp image
    if os.path.exists(fnmq):
        os.remove(fnmq)

    # draw other lines to pdf
    pg.draw_line((15, 435), (785, 435), width=3, color=(0, 0, 0, 1))
    pg.draw_line((260, 435), (260, 655), width=3, color=(0, 0, 0, 1))
    pg.draw_line((15, 655), (785, 655), width=3, color=(0, 0, 0, 1))

    # routing text
    rts = 'SJC'
    pg.insert_text((310, 505), rts, fontsize=fsz_5, color=fitz.utils.getColor('black'), render_mode=2)
    rts = '951'
    pg.insert_text((460, 505), rts, fontsize=fsz_5, color=fitz.utils.getColor('black'), render_mode=2)
    rts = '31'
    pg.insert_text((560, 505), rts, fontsize=fsz_5, color=fitz.utils.getColor('black'))
    rts = 'A1'
    pg.insert_text((660, 505), rts, fontsize=fsz_5, color=fitz.utils.getColor('black'))

    # routing barcode
    img = barcode.Code128('95131', writer=barcode.writer.ImageWriter())
    fnmq = img.save(os.path.join(cfg.LBLPDFt, 'SZ405BGP0300050198' + '-b'), options={"write_text": False})
    pg.insert_image((270, 520, 780, 645), filename=fnmq)
    if os.path.exists(fnmq):
        os.remove(fnmq)

    # main barcode
    pg.draw_line((15, 1015), (785, 1015), width=8, color=(0, 0, 0, 1))
    # add barcode
    img = barcode.Code128('SZ405BGP0300050198', writer=barcode.writer.ImageWriter())
    fnmq = img.save(os.path.join(cfg.LBLPDFt, 'SZ405BGP0300050198' + '-b'), options={"write_text": False})
    pg.insert_image((20, 800, 780, 995), filename=fnmq)
    if os.path.exists(fnmq):
        os.remove(fnmq)

    doc.save(f)

# create pdf with reportlab
f = os.path.join(cfg.LBLPDFt, 'testrl.pdf')
# page size 800px X 1200px
pg_size = (800, 1200)
# initiate a canvas object to hold pdf content
cvs = Canvas(f, pagesize=pg_size)
# outside border
cvs.setLineWidth(1)
cvs.line(10, 10, 790, 10)
cvs.line(790, 10, 790, 1190)
cvs.line(10, 10, 10, 1190)
cvs.line(10, 1190, 790, 1190)
# Settings: font size
fsz_1 = 28
fsz_2 = 40
fsz_3 = 36
fsz_4 = 48
fsz_5 = 64
fsz_6 = 24

# insert qcode
qrc = qr.QrCodeWidget('http://www.bzking.net', barLevel='H', barWidth=10, barHeight=10)
bds = qrc.getBounds()
w = bds[2] - bds[0]
h = bds[3] - bds[1]
d = Drawing(240, 240, transform=[240./w, 0, 0, 240./h, 0, 0])
d.add(qrc)
d.drawOn(cvs, 15, 525)
cvs.line(10, 755, 790, 755)
cvs.line(260, 755, 260, 535)
cvs.line(10, 535, 790, 535)

# routing text
rts = 'SJC'
cvs.setFont('Helvetica-Bold', fsz_5)
cvs.drawString(310, 685, rts)
rts = '951'
cvs.drawString(460, 685, rts)
cvs.setFont('Helvetica', fsz_5)
rts = '31'
cvs.drawString(560, 685, rts)
rts = 'A1'
cvs.drawString(660, 685, rts)
# routing barcode
b = code128.Code128('95131', barWidth=2.5, barHeight=100)
b.drawOn(cvs, 400, 550)

# Barcode
cvs.setLineWidth(5)
cvs.line(10, 175, 790, 175)
# add barcode
b = code128.Code128('SZ405BGP0300050198', barWidth=2.5, barHeight=180)
b.drawOn(cvs, 145, 205)

cvs.showPage()
cvs.save()
