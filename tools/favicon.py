"""Favicon (v3, 19/10): só o B em Cinzel Decorative Black, em café, centralizado pela tinta da letra
(não pela caixa do texto), sobre um quadrado de cantos arredondados em degradê bronze com um fio claro por dentro.
v1 (B fino do logo sobre café) sumia na aba; v2 tinha a estrela, que o usuário tirou para ficar minimalista.
Fonte em ../_ref/fontes/CinzelDecorative.ttf. O processar.py chama este arquivo."""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
FONTE = os.path.join(SITE, '..', '_ref', 'fontes', 'CinzelDecorative.ttf')
CAFE = (24, 17, 13)
BRONZE_CLARO, BRONZE = (222, 180, 130), (150, 99, 55)


def favicon(S, cantos=True):
    k = 8; s = S * k
    raio = int(s * .23) if cantos else 0
    fundo = Image.new('RGBA', (s, s))
    fd = ImageDraw.Draw(fundo)
    for y in range(s):  # degradê na diagonal suave: luz de cima
        t = y / s
        fd.line((0, y, s, y), fill=tuple(int(BRONZE_CLARO[i] * (1 - t) + BRONZE[i] * t) for i in range(3)) + (255,))
    m = Image.new('L', (s, s))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), radius=raio, fill=255)
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    im.paste(fundo, (0, 0), m)
    if S >= 48:  # fio claro por dentro, só onde dá para ver
        e = int(s * .045)
        ImageDraw.Draw(im).rounded_rectangle((e, e, s - 1 - e, s - 1 - e), radius=max(raio - e, 0),
                                             outline=(246, 226, 196, 80), width=max(k, int(s * .006)))
    # a letra numa camada própria, para medir a tinta e centralizar de verdade
    f = ImageFont.truetype(FONTE, int(s * (.72 if S >= 48 else .8)))
    camada = Image.new('L', (s * 2, s * 2))
    ImageDraw.Draw(camada).text((s // 2, s // 2), 'B', font=f, fill=255)
    caixa = camada.getbbox()
    letra = camada.crop(caixa)
    x = (s - letra.width) // 2
    y = (s - letra.height) // 2
    cor = Image.new('RGBA', letra.size, CAFE + (255,))
    im.paste(cor, (x, y), letra)
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
