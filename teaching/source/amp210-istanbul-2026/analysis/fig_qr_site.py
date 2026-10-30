"""QR code for josephphall.com (title slide corner + credits frame).

Requires qrcode[pil]: pip3 install --user "qrcode[pil]".
"""
import os
import qrcode
from common import DECK

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                   box_size=12, border=2)
qr.add_data('https://josephphall.com')
qr.make(fit=True)
img = qr.make_image(fill_color='#003057', back_color='white')
img.save(os.path.join(DECK, 'fig_qr_site.png'))
print('  wrote fig_qr_site.png', img.size)
