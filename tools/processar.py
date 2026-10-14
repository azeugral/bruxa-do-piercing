"""Gera assets/obras/*.webp, assets/js/obras.js, o logo da Bruxa, as fotos da Moni, favicons e og-bruxa.jpg.

Originais em ../_ref/ig (extraídos do Instagram @bruxadopiercing em 13/10/2026).
Os números são os da folha de contato ../_ref/contato/*.jpg e da lista ../_ref/legendas.txt
(000 = post mais recente). As legendas resumem o que ela mesma escreveu no post (joia, perfuração).
"""
import glob, json, os
from PIL import Image, ImageOps, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(SITE, '..', '_ref')
IG = os.path.join(REF, 'ig')
OUT = os.path.join(SITE, 'assets', 'obras')
IMG = os.path.join(SITE, 'assets', 'img')

CAFE = (22, 16, 13)
OSSO = (236, 228, 214)

O, R, C, E = 'orelha', 'rosto', 'corpo', 'ensaios'
OBRAS = {
  # orelha
  '000': (O, 'Dois projetos auriculares numa orelha'), '037': (O, 'Projeto auricular'), '047': (O, 'Projeto auricular com pontos de luz'),
  '060': (O, 'Projeto auricular, nova versão'), '065': (O, 'Forward helix em folha'), '089': (O, 'Orelhinhas do ensaio no café'),
  '140': (O, 'Expansão de lóbulo, 2 a 5 mm'), '145': (O, 'Projeto em andamento'), '147': (O, 'Joias de ouro'),
  '152': (O, 'Projeto auricular'), '161': (O, 'Trinity, Primavera e Hebe ametista'), '163': (O, 'Daith com joia Agnes'),
  '168': (O, 'Trinity zircônia e Litha'), '170': (O, 'Celta e ponto de luz'), '177': (O, 'Aurora zircônia'),
  '180': (O, 'Trago com joia Fada'), '184': (O, 'Projeto auricular Ondina'), '186': (O, 'Mabon, Litha e navete'),
  '191': (O, 'Projeto auricular Aura’s'), '192': (O, 'Rook, scapha e conch'), '196': (O, 'Joias anodizadas'),
  '200': (O, 'Hélix, scapha, conch e lóbulo'), '203': (O, 'Daith, trago e lóbulo'), '204': (O, 'Hélix e rook'),
  '207': (O, 'Triple hélix'),
  # rosto
  '012': (R, 'Olhos de aranha'), '018': (R, 'Bridge e Dhalia'), '020': (R, 'Venom anodizado em purple'),
  '045': (R, 'Nasallang'), '070': (R, 'Double Ashley'), '072': (R, 'Hi nostril'), '073': (R, 'Snake bites'),
  '075': (R, 'Clown eyes'), '081': (R, 'Joias anodizadas em dourado'), '083': (R, 'Medusa com Ivy Esmeralda'),
  '084': (R, 'Vertical labret e sobrancelha'), '085': (R, 'Projeto facial em dark bronze'), '093': (R, 'Double nostril'),
  '094': (R, 'Septo e argola cravejada'), '097': (R, 'Nostril'), '101': (R, 'Projeto facial'), '106': (R, 'Medusa com topo Eros'),
  '114': (R, 'Spike'), '123': (R, 'Projeto facial'), '126': (R, 'Dermal com zircônia azul'), '142': (R, 'Projeto facial'),
  '153': (R, 'Dark Snake e Ivy Esmeralda'), '156': (R, 'Septo com ferradura spike'), '162': (R, 'Vertical labret'),
  '169': (R, 'Agnes e labret'), '175': (R, 'Cores & Poesia'), '185': (R, 'Vertical labret com topo disco'),
  '189': (R, 'Septo com joia Perseu'), '197': (R, 'Septo anodizado em 65v'), '198': (R, 'Projeto facial'),
  '199': (R, 'Atualização de joia'), '201': (R, 'Joia anodizada em 20v'),
  # corpo
  '001': (C, 'Umbigo'), '041': (C, 'Umbigo'), '068': (C, 'Triplo dermal no colo'), '071': (C, 'Umbigo triplo'),
  '128': (C, 'Surface no colo'), '139': (C, 'Troca para titânio'), '158': (C, 'Surface no colo'), '160': (C, 'Mamilo'),
  '178': (C, 'Navel com joia Fantine'), '202': (C, 'Surface no esterno'),
  # ensaios
  '039': (E, 'Yule · olhos de aranha'), '035': (E, 'Imbolc'), '038': (E, 'Nostril e henna'), '050': (E, 'Boitatá'),
  '052': (E, 'Samhain · corset em play piercing'), '053': (E, 'Back dermal'), '055': (E, 'Mabon'), '058': (E, 'Lammas'),
  '076': (E, 'Ensaio no café'), '086': (E, 'Orelha na neve'), '059': (E, 'Joia Fúlvia'), '088': (E, 'Orc fangs'),
}


def salvar(im, pasta, nome, larguras=(640, 1200), q=80):
    for w in larguras:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(os.path.join(pasta, f'{nome}-{w}.webp'), 'WEBP', quality=q, method=6)


def logo():
    """logo oficial (marca d'água da foto 150): osso sobre a camiseta vermelha.
    Alfa vem do canal azul (o fundo vermelho quase não tem azul); depois é ampliado e afinado."""
    im = Image.open(os.path.join(IG, '150.webp')).convert('RGB').crop((1086, 1528, 1362, 1716))
    b = im.split()[2]
    lo, hi = 70, 190
    a = b.point(lambda v: 0 if v <= lo else 255 if v >= hi else int((v - lo) * 255 / (hi - lo)))
    a = a.resize((a.width * 4, a.height * 4), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
    a = a.point(lambda v: 0 if v < 80 else 255 if v > 175 else int((v - 80) * 255 / 95))
    a = a.crop(a.getbbox())
    claro = Image.new('RGBA', a.size, OSSO + (0,)); claro.putalpha(a)
    escuro = Image.new('RGBA', a.size, CAFE + (0,)); escuro.putalpha(a)
    claro.save(os.path.join(IMG, 'logo-bruxa.png'))
    escuro.save(os.path.join(IMG, 'logo-bruxa-escuro.png'))
    for w in (300, 600):
        claro.resize((w, round(a.height * w / a.width)), Image.LANCZOS).save(os.path.join(IMG, f'logo-bruxa-{w}.webp'), 'WEBP', quality=92, method=6)
    return claro


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.webp')):
        os.remove(f)
    lista = []
    for i in sorted(OBRAS):
        cat, desc = OBRAS[i]
        im = ImageOps.exif_transpose(Image.open(os.path.join(IG, i + '.webp'))).convert('RGB')
        nome = f'bp-{i}'
        salvar(im, OUT, nome)
        lista.append({'id': nome, 'e': cat, 'd': desc, 'r': round(im.width / im.height, 3)})
    open(os.path.join(SITE, 'assets', 'js', 'obras.js'), 'w', encoding='utf-8').write(
        'window.OBRAS = ' + json.dumps(lista, ensure_ascii=False, separators=(',', ':')) + ';\n')

    lg = logo()

    # abertura: ensaio de Yule (olhos de aranha), sobre: foto de perfil dela, estúdio: o post do coven
    salvar(Image.open(os.path.join(IG, '039.webp')).convert('RGB'), IMG, 'yule', (640, 1200), 84)
    salvar(Image.open(os.path.join(IG, 'perfil.jpg')).convert('RGB'), IMG, 'moni', (480, 900), 84)
    salvar(Image.open(os.path.join(IG, '079.webp')).convert('RGB'), IMG, 'coven', (640, 1200), 84)

    # favicon: o "U" com a estrela do logo, recortado do logo, sobre café
    u = lg.crop((round(lg.width * .395), 0, round(lg.width * .585), round(lg.height * .66)))
    u = u.crop(u.getbbox())
    for s, nome in ((32, 'favicon-32.png'), (180, 'assets/img/icone-180.png'), (512, 'assets/img/icone-512.png')):
        fav = Image.new('RGBA', (s, s), CAFE + (255,))
        e = u.copy()
        e.thumbnail((int(s * .62), int(s * .8)), Image.LANCZOS)
        fav.alpha_composite(e, ((s - e.width) // 2, (s - e.height) // 2))
        fav.convert('RGB').save(os.path.join(SITE, nome))
    Image.open(os.path.join(SITE, 'assets/img/icone-512.png')).save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])

    # prévia de link 1200x630: logo no quadrado do meio, fotos nas laterais
    og = Image.new('RGB', (1200, 630), CAFE)
    def lado(foto, x, centro=(.5, .4)):
        f = ImageOps.fit(foto, (260, 630), Image.LANCZOS, centering=centro)
        g = Image.new('L', (260, 630))
        gd = ImageDraw.Draw(g)
        for k in range(260):
            gd.line((k, 0, k, 630), fill=int(235 * (k / 260 if x else 1 - k / 260)))
        og.paste(f, (x, 0), g)
    lado(Image.open(os.path.join(IG, '039.webp')).convert('RGB'), 0)
    lado(Image.open(os.path.join(IG, '192.webp')).convert('RGB'), 940)
    l2 = lg.copy()
    l2.thumbnail((520, 300), Image.LANCZOS)
    og.paste(l2, ((1200 - l2.width) // 2, (630 - l2.height) // 2), l2)
    og.save(os.path.join(SITE, 'og-bruxa.jpg'), quality=86)
    print(len(lista), 'fotos')


if __name__ == '__main__':
    main()
