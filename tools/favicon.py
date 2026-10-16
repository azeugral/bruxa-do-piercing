"""Favicon: o B do logo dela (recortado de assets/img/logo-bruxa.png) em osso, sobre um quadrado café
de cantos arredondados, com a estrela do logo em bronze. Rodar depois do processar.py."""
import os
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
CAFE, OSSO, BRONZE = (22, 16, 13), (236, 228, 214), (181, 128, 76)

logo = Image.open(os.path.join(SITE, 'assets', 'img', 'logo-bruxa.png'))
B = logo.crop((0, 60, 175, 560)); B = B.crop(B.getbbox())


def so_estrela():
    """a estrela encosta no U: separa só a peça conectada que contém o centro dela"""
    r = logo.crop((420, 0, 580, 140)); a = r.split()[3].point(lambda v: 255 if v > 60 else 0)
    w, h = a.size; px = a.load(); vis = set(); fila = [(77, 40)]
    while fila:
        x, y = fila.pop()
        if (x, y) in vis or not (0 <= x < w and 0 <= y < h) or not px[x, y]:
            continue
        vis.add((x, y)); fila += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    m = Image.new('L', (w, h)); mp = m.load()
    for x, y in vis:
        mp[x, y] = 255
    m = m.filter(ImageFilter.MaxFilter(3))
    out = r.copy(); out.putalpha(Image.composite(r.split()[3], Image.new('L', (w, h)), m))
    return out.crop(out.getbbox())


ESTRELA = so_estrela()


def pintar(peca, cor, altura, engrossar=0, largura=1.0):
    # largura > 1 abre o B, que no logo é bem condensado e some em 32 px
    p = peca.resize((round(peca.width * altura / peca.height * largura), altura), Image.LANCZOS)
    a = p.split()[3]
    if engrossar:  # nos tamanhos pequenos os fios finos do B somem
        a = a.filter(ImageFilter.MaxFilter(engrossar))
    out = Image.new('RGBA', p.size, cor + (0,))
    out.putalpha(a)
    return out


def favicon(S, engrossar=0, cantos=True):
    k = 4; s = S * k
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .23) if cantos else 0, fill=CAFE + (255,))
    b = pintar(B, OSSO, int(s * .6), engrossar, 1.55)
    x = (s - b.width) // 2 - int(s * .03); y = (s - b.height) // 2 + int(s * .04)
    im.alpha_composite(b, (x, y))
    e = pintar(ESTRELA, BRONZE, int(s * .19))
    im.alpha_composite(e, (x + b.width - e.width // 6, y - int(e.height * .72)))
    return im.resize((S, S), Image.LANCZOS)


favicon(32, 7).save(os.path.join(SITE, 'favicon-32.png'))
favicon(512).save(os.path.join(SITE, 'assets', 'img', 'icone-512.png'))
favicon(180, cantos=False).convert('RGB').save(os.path.join(SITE, 'assets', 'img', 'icone-180.png'))  # o iOS já arredonda
ico = [favicon(16, 9), favicon(32, 7), favicon(48, 5)]
ico[2].save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
prev = Image.new('RGB', (512 + 180 + 64 + 48 + 32 + 16 + 90, 512), (240, 236, 230)); x = 0
for S, g in ((512, 0), (180, 0), (64, 5), (48, 5), (32, 7), (16, 9)):
    f = favicon(S, g); prev.paste(f, (x, 0), f); x += S + 15
prev.save(os.path.join(SITE, '..', '_ref', 'favicon-preview.png'))
print('ok')
