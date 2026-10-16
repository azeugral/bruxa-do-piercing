# Bruxa do Piercing

Site da Moni ([@bruxadopiercing](https://www.instagram.com/bruxadopiercing/)), body piercer em Joinville, SC, no estúdio O Coven ([@ocoven.estudioo](https://www.instagram.com/ocoven.estudioo/)).

Prévia: https://azeugral.github.io/bruxa-do-piercing/ (com `noindex` até ter domínio).

## Identidade (v1, 14/10/2026)

- **Logo:** o oficial dela, "BRUXA do piercing" com a estrela em cima do U. Recortado da marca d'água da foto 150 (`../_ref/ig/150.webp`) e convertido para fundo transparente por `tools/processar.py`. Ela deve ter o arquivo original em vetor: pedir e trocar.
- **Favicon (v2, 16/10):** B em Cinzel Decorative Black (capitular com cauda em gancho) em café, sobre quadrado de cantos arredondados em degradê bronze, com a estrela de 4 pontas em osso. Lê bem em 16 e 32 px nas abas clara e escura. Gerado por `tools/favicon.py` (fonte em `../_ref/fontes`).
- **Cores:** café `#16100d`, osso `#ece4d6` (a cor do logo) e bronze `#b5804c` (claro `#d9ab78`). É a anodização dark bronze e o 🤎 que ela usa nas legendas.
- **Fontes:** Marcellus nos títulos e IBM Plex Sans no texto.
- **Layout:** nav convencional com o logo à esquerda e o menu à direita (gaveta abaixo de 1100 px), seções simétricas.
- **Botões:** retos, osso, com a estrela numa célula própria. No hover, o bronze sobe de baixo e a estrela gira.

## Estrutura

| Arquivo | O que é |
|---|---|
| `index.html` | Abertura, próximas datas, perfurações, trabalhos recentes, joias e materiais, cicatrização, ensaios, O Coven, sobre, cursos, cupons e chamada |
| `trabalhos.html` | Portfólio com filtro Orelha, Rosto, Corpo e Ensaios (`?cat=`) e lightbox |
| `agendar.html` | Monta a mensagem e abre o WhatsApp `5547991017599`. Aceita `?cidade=sp` ou `curitiba` e `?tipo=exotica` ou `curso` |
| `assets/js/site.js` | `CONFIG` (Instagram e WhatsApp) e o comportamento do site |
| `assets/js/obras.js` | Gerado. Não editar à mão |

## Fluxo

```bash
python tools/processar.py      # fotos de ../_ref/ig -> assets/obras + obras.js, logo, fotos, favicons, og-bruxa.jpg
python tools/montar_paginas.py # tools/paginas/*.html -> páginas da raiz (V = cache)
```

Os originais vieram do Instagram dela (os 208 posts, em 13/10/2026). Estão em `../_ref/ig`, com as legendas em `../_ref/legendas.txt` e as folhas de contato em `../_ref/contato`.

## CONFIRMAR

Os itens pendentes aparecem no site como "✦ a preencher", com sublinhado tracejado.

- [ ] **Datas de viagem** (seção "Próximas datas" e opções do `agendar.html`): SP 29/10 a 03/11, Curitiba 05/11 e Tattoo Ink Pinhais 06 a 08/11. São as da bio em 13/10. **Vencem em novembro.** Atualizar ou esconder a faixa depois disso.
- [ ] **Endereço e horários** do Coven.
- [ ] **Valores** das perfurações, ou "sob consulta".
- [ ] **Cursos:** a bio diz "Agenda • Cursos • Informações", mas o link da bio não abriu. Faltam datas, formato e conteúdo.
- [ ] **Menores de idade:** o site diz "só com responsável presente". Confirmar a regra dela (idade mínima, autorização).
- [ ] **Cicatrização:** os nomes das três fases são os de uso geral. Ela fala em "três fases" sem nomear. Faltam os cuidados por escrito e o retorno de downsize.
- [ ] **Cupons:** BRUXA15OFF (Tribo do Sol), BRUXA15 (Desire) e BRUXA (Guimed) saíram de legendas. Confirmar se continuam valendo.
- [ ] **Logo em vetor:** o atual foi tirado de uma foto e serve até uns 300 px de largura.
- [ ] **Domínio:** quando houver, trocar `BASE` em `tools/montar_paginas.py`, tirar o `noindex` e trocar o `robots.txt`.
