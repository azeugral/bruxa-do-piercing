"""Favicon (v2, 16/10): B em Cinzel Decorative Black (capitular com a cauda em gancho, o lado "bruxa"),
em café, sobre um quadrado de cantos arredondados em degradê bronze, com a estrela de 4 pontas do logo em osso.
A v1 (o B fino do logo em osso sobre café) virou "um quadrado escuro" na aba: o fundo claro e a letra
grossa é o que aparece em 16 e 32 px, tanto na aba clara quanto na escura.
Fonte em ../_ref/fontes/CinzelDecorative.ttf. Rodar depois do processar.py (ele chama este arquivo)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
FONTE = os.path.join(SITE, '..', '_ref', 'fontes', 'CinzelDecorative.ttf')
CAFE, OSSO = (22, 16, 13), (240, 232, 218)
BRONZE_CLARO, BRONZE = (219, 174, 122), (156, 104, 58)


def estrela(d, cx, cy, r, cor):
    """astroide: a estrela de 4 pontas finas do logo"""
    d.polygon([(cx + r * math.cos(t) ** 3, cy + r * math.sin(t) ** 3)
               for t in (k / 96 * 2 * math.pi for k in range(96))], fill=cor)


def favicon(S, cantos=True):
    k = 8; s = S * k
    fundo = Image.new('RGBA', (s, s))
    fd = ImageDraw.Draw(fundo)
    for y in range(s):
        t = y / s
        fd.line((0, y, s, y), fill=tuple(int(BRONZE_CLARO[i] * (1 - t) + BRONZE[i] * t) for i in range(3)) + (255,))
    m = Image.new('L', (s, s))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .24) if cantos else 0, fill=255)
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    im.paste(fundo, (0, 0), m)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONTE, int(s * .8))
    bb = d.textbbox((0, 0), 'B', font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    x = (s - w) / 2 - bb[0] - s * .07
    y = (s - h) / 2 - bb[1] + s * .04
    d.text((x, y), 'B', font=f, fill=CAFE)
    estrela(d, x + bb[0] + w + s * .01, y + bb[1] + s * .03, s * .11, OSSO)
    return im.resize((S, S), Image.LANCZOS)


favicon(32).save(os.path.join(SITE, 'favicon-32.png'))
favicon(512).save(os.path.join(SITE, 'assets', 'img', 'icone-512.png'))
favicon(180, cantos=False).convert('RGB').save(os.path.join(SITE, 'assets', 'img', 'icone-180.png'))  # o iOS já arredonda
ico = [favicon(16), favicon(32), favicon(48)]
ico[2].save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])

# prévia: abas clara e escura, nos tamanhos reais e ampliado
prev = Image.new('RGB', (760, 300), (246, 243, 238))
ImageDraw.Draw(prev).rectangle((0, 150, 760, 300), fill=(32, 33, 36))
for fy in (0, 150):
    x = 15
    for S in (128, 64, 48, 32, 16):
        i = favicon(S); prev.paste(i, (x, fy + 11 + (128 - S) // 2), i); x += S + 40
prev.save(os.path.join(SITE, '..', '_ref', 'favicon-preview.png'))
print('ok')
