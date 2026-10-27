#!/usr/bin/env python3
"""
Gera o ebook PDF: Inglês Britânico & Irlandês para Iniciantes
"""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Flowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "images"
OUT = ROOT / "Ingles_Britanico_Irlandes_para_Iniciantes.pdf"

# Paleta: campo britânico / costa irlandesa (sem roxo)
FOREST = colors.HexColor("#1F4D3A")
SAGE = colors.HexColor("#4A7C59")
MIST = colors.HexColor("#E8F0EA")
IVORY = colors.HexColor("#F7F4EF")
INK = colors.HexColor("#1C2421")
TEA = colors.HexColor("#C45C26")
SOFT = colors.HexColor("#D9E5DC")
LINE = colors.HexColor("#A8C0B0")
WHITE = colors.white


def register_fonts() -> dict[str, str]:
    """Tenta fontes expressivas do sistema; cai para Helvetica se preciso."""
    candidates = {
        "display": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        ],
        "body": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
        "body_bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "italic": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        ],
        "mono": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        ],
    }
    names = {}
    for key, paths in candidates.items():
        for p in paths:
            if os.path.exists(p):
                fname = f"Ebook{key.title().replace('_', '')}"
                pdfmetrics.registerFont(TTFont(fname, p))
                names[key] = fname
                break
        else:
            names[key] = {
                "display": "Times-Bold",
                "body": "Helvetica",
                "body_bold": "Helvetica-Bold",
                "italic": "Times-Italic",
                "mono": "Courier",
            }[key]
    return names


FONTS = register_fonts()


def make_styles():
    ss = getSampleStyleSheet()
    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName=FONTS["display"],
            fontSize=28,
            leading=34,
            textColor=FOREST,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName=FONTS["italic"],
            fontSize=14,
            leading=20,
            textColor=SAGE,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName=FONTS["body"],
            fontSize=11,
            leading=16,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=FONTS["display"],
            fontSize=20,
            leading=26,
            textColor=FOREST,
            spaceBefore=4,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=FONTS["body_bold"],
            fontSize=13,
            leading=18,
            textColor=SAGE,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName=FONTS["body_bold"],
            fontSize=11,
            leading=15,
            textColor=FOREST,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=FONTS["body"],
            fontSize=10,
            leading=15,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            fontName=FONTS["body"],
            fontSize=10,
            leading=14,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "en": ParagraphStyle(
            "en",
            fontName=FONTS["body_bold"],
            fontSize=10.5,
            leading=15,
            textColor=FOREST,
            spaceAfter=2,
        ),
        "pt": ParagraphStyle(
            "pt",
            fontName=FONTS["body"],
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#3A4A42"),
            spaceAfter=6,
        ),
        "tip": ParagraphStyle(
            "tip",
            fontName=FONTS["body"],
            fontSize=9.5,
            leading=13.5,
            textColor=INK,
            alignment=TA_LEFT,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName=FONTS["italic"],
            fontSize=9,
            leading=12,
            textColor=SAGE,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12,
        ),
        "toc": ParagraphStyle(
            "toc",
            fontName=FONTS["body"],
            fontSize=11,
            leading=20,
            textColor=INK,
        ),
        "dialogue_en": ParagraphStyle(
            "dialogue_en",
            fontName=FONTS["body"],
            fontSize=10,
            leading=14,
            textColor=FOREST,
            leftIndent=8,
            spaceAfter=2,
        ),
        "dialogue_pt": ParagraphStyle(
            "dialogue_pt",
            fontName=FONTS["italic"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#556B5E"),
            leftIndent=8,
            spaceAfter=6,
        ),
        "exercise": ParagraphStyle(
            "exercise",
            fontName=FONTS["body"],
            fontSize=10,
            leading=14,
            textColor=INK,
            spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName=FONTS["body"],
            fontSize=8,
            textColor=SAGE,
            alignment=TA_CENTER,
        ),
        "small": ParagraphStyle(
            "small",
            fontName=FONTS["body"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#4A5C52"),
            alignment=TA_CENTER,
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName=FONTS["body"],
            fontSize=9,
            leading=12,
            textColor=INK,
        ),
        "cell_b": ParagraphStyle(
            "cell_b",
            fontName=FONTS["body_bold"],
            fontSize=9,
            leading=12,
            textColor=FOREST,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            fontName=FONTS["body_bold"],
            fontSize=9,
            leading=12,
            textColor=WHITE,
        ),
    }
    return styles


S = make_styles()


class AccentBar(Flowable):
    def __init__(self, width=16 * cm, height=3):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(SAGE)
        self.canv.rect(0, 0, self.width * 0.55, self.height, fill=1, stroke=0)
        self.canv.setFillColor(TEA)
        self.canv.rect(self.width * 0.55, 0, self.width * 0.2, self.height, fill=1, stroke=0)
        self.canv.setFillColor(FOREST)
        self.canv.rect(self.width * 0.75, 0, self.width * 0.25, self.height, fill=1, stroke=0)


class TipBox(Flowable):
    """Caixa de dica com fundo sage suave."""

    def __init__(self, title: str, text: str, width=16 * cm):
        super().__init__()
        self.title = title
        self.text = text
        self.box_width = width
        self._paragraphs = None
        self.height = 0

    def wrap(self, availWidth, availHeight):
        w = min(self.box_width, availWidth)
        title_p = Paragraph(f"<b>{self.title}</b>", S["tip"])
        body_p = Paragraph(self.text, S["tip"])
        tw, th = title_p.wrap(w - 16, availHeight)
        bw, bh = body_p.wrap(w - 16, availHeight)
        self._paragraphs = (title_p, body_p, tw, th, bw, bh)
        self.height = th + bh + 18
        self.width = w
        return w, self.height

    def draw(self):
        title_p, body_p, tw, th, bw, bh = self._paragraphs
        c = self.canv
        c.setFillColor(MIST)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=1)
        c.setFillColor(TEA)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        title_p.drawOn(c, 12, self.height - th - 8)
        body_p.drawOn(c, 12, 8)


def img(name: str, width=15 * cm, max_height=8.5 * cm) -> list:
    path = IMG / name
    if not path.exists():
        return []
    im = Image(str(path))
    iw, ih = im.imageWidth, im.imageHeight
    ratio = iw / ih
    w = width
    h = w / ratio
    if h > max_height:
        h = max_height
        w = h * ratio
    im.drawWidth = w
    im.drawHeight = h
    return [im]


def vocab_table(rows: list[tuple[str, str, str]], col_headers=None):
    headers = col_headers or ("English (UK/IE)", "Pronúncia aproximada", "Português")
    data = [[Paragraph(h, S["cell_head"]) for h in headers]]
    for a, b, c in rows:
        data.append(
            [
                Paragraph(a, S["cell_b"]),
                Paragraph(b, S["cell"]),
                Paragraph(c, S["cell"]),
            ]
        )
    t = Table(data, colWidths=[5.2 * cm, 5.2 * cm, 5.2 * cm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), FOREST),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), IVORY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [IVORY, MIST]),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def phrase_pair(en: str, pt: str) -> list:
    return [Paragraph(en, S["en"]), Paragraph(pt, S["pt"])]


def dialogue_line(who: str, en: str, pt: str) -> list:
    return [
        Paragraph(f"<b>{who}:</b> {en}", S["dialogue_en"]),
        Paragraph(pt, S["dialogue_pt"]),
    ]


def chapter_header(number: str, title: str) -> list:
    return [
        Paragraph(f"Capítulo {number}", S["pt"]),
        Paragraph(title, S["h1"]),
        AccentBar(),
        Spacer(1, 10),
    ]


def add_page_decorations(canvas, doc):
    canvas.saveState()
    page = doc.page
    # margem decorativa superior
    canvas.setFillColor(FOREST)
    canvas.rect(0, A4[1] - 8, A4[0], 8, fill=1, stroke=0)
    canvas.setFillColor(SAGE)
    canvas.rect(0, 0, A4[0], 14, fill=1, stroke=0)
    if page > 1:
        canvas.setFillColor(WHITE)
        canvas.setFont(FONTS["body"], 8)
        canvas.drawCentredString(
            A4[0] / 2,
            4,
            f"Inglês Britânico & Irlandês para Iniciantes  ·  {page}",
        )
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.0 * cm,
        title="Inglês Britânico & Irlandês para Iniciantes",
        author="Ebook Didático — British & Irish English",
        subject="Curso iniciante de inglês britânico e irlandês",
    )
    story: list = []

    # ========== CAPA ==========
    story.extend(img("cover.jpg", width=16 * cm, max_height=9 * cm))
    story.append(Spacer(1, 14))
    story.append(AccentBar())
    story.append(Spacer(1, 14))
    story.append(Paragraph("English from These Isles", S["cover_title"]))
    story.append(
        Paragraph(
            "Inglês Britânico & Irlandês para Iniciantes",
            S["cover_sub"],
        )
    )
    story.append(
        Paragraph(
            "Um guia visual e prático para quem está começando do zero —<br/>"
            "com foco em inglês do Reino Unido e da Irlanda.",
            S["cover_meta"],
        )
    )
    story.append(Spacer(1, 18))
    story.append(
        Paragraph(
            "Nível A1 → A2  ·  Explicações em português  ·  Exercícios inclusos",
            S["small"],
        )
    )
    story.append(PageBreak())

    # ========== COMO USAR ==========
    story.extend(chapter_header("0", "Como usar este ebook"))
    story.append(
        Paragraph(
            "Este livro foi feito para quem nunca estudou inglês — ou já tentou e "
            "quer recomeçar com calma. As explicações estão em <b>português</b>; "
            "os exemplos e diálogos usam <b>inglês britânico</b>, com notas sobre "
            "o inglês falado na <b>Irlanda</b>.",
            S["body"],
        )
    )
    story.append(Paragraph("Método em 4 passos", S["h2"]))
    for step in [
        "<b>1. Ouça na cabeça.</b> Leia cada frase em voz alta. O inglês britânico "
        "tem sons que o português não tem — treinar a boca ajuda mais do que decorar.",
        "<b>2. Compare.</b> Cada frase em inglês vem com tradução. Não traduza palavra "
        "por palavra: sinta o sentido completo.",
        "<b>3. Repita sem olhar.</b> Tape a tradução e diga a frase de novo.",
        "<b>4. Pratique os exercícios.</b> No fim de cada bloco há treinos curtos. "
        "As respostas estão no Capítulo 12.",
    ]:
        story.append(Paragraph(step, S["body_left"]))
        story.append(Spacer(1, 4))

    story.append(
        TipBox(
            "Dica de ouro",
            "Prefira 20 minutos por dia a 3 horas no sábado. O cérebro aprende "
            "idioma com repetição espaçada — como café da manhã, não como banquete.",
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph("Sobre o inglês destas ilhas", S["h2"]))
    story.extend(img("uk-ireland.jpg", width=15 * cm, max_height=7 * cm))
    story.append(
        Paragraph(
            "Reino Unido (Inglaterra, Escócia, País de Gales, Irlanda do Norte) e Irlanda.",
            S["caption"],
        )
    )
    story.append(
        Paragraph(
            "O inglês britânico padrão (Received Pronunciation / Southern British) "
            "é o modelo de pronúncia deste livro. O inglês irlandês (Hiberno-English) "
            "é inteligível para qualquer falante de inglês, mas tem ritmo, vocabulário "
            "e construções próprias — você verá notas <b>[IE]</b> ao longo do texto.",
            S["body"],
        )
    )
    story.append(PageBreak())

    # ========== SUMÁRIO ==========
    story.append(Paragraph("Sumário", S["h1"]))
    story.append(AccentBar())
    story.append(Spacer(1, 10))
    toc = [
        "0 — Como usar este ebook",
        "1 — O alfabeto e a pronúncia britânica",
        "2 — Cumprimentos e primeiras conversas",
        "3 — Números, dias, meses e horas",
        "4 — Família e pessoas",
        "5 — Vida quotidiana (daily life)",
        "6 — Comida e bebida (UK & Ireland)",
        "7 — Gramática essencial do iniciante",
        "8 — Lugares, direções e viagem",
        "9 — Inglês irlandês: o que notar",
        "10 — Britânico × Americano (diferenças úteis)",
        "11 — Diálogos para praticar",
        "12 — Exercícios + respostas",
        "Glossário rápido A–Z",
    ]
    for item in toc:
        story.append(Paragraph(item, S["toc"]))
    story.append(PageBreak())

    # ========== CAP 1 ALFABETO ==========
    story.extend(chapter_header("1", "O alfabeto e a pronúncia britânica"))
    story.append(
        Paragraph(
            "O inglês usa as mesmas 26 letras do alfabeto latino. A diferença está "
            "nos <b>sons</b>. Abaixo, a leitura aproximada para brasileiros, no "
            "estilo britânico.",
            S["body"],
        )
    )
    story.append(Paragraph("O alfabeto (British English)", S["h2"]))
    alphabet = [
        ("A", "ei", "como em “hey”"),
        ("B", "bi", ""),
        ("C", "ci", "som de “ssí”"),
        ("D", "di", ""),
        ("E", "i", "como “ee” longo"),
        ("F", "éf", ""),
        ("G", "dji", ""),
        ("H", "êitch", "o H britânico é aspirado"),
        ("I", "ai", ""),
        ("J", "djei", ""),
        ("K", "kei", ""),
        ("L", "él", ""),
        ("M", "ém", ""),
        ("N", "én", ""),
        ("O", "ou", "como “oh”"),
        ("P", "pi", ""),
        ("Q", "kiu", ""),
        ("R", "á", "R britânico é suave; no final quase some"),
        ("S", "éss", ""),
        ("T", "ti", "T claro (não vira “rá” como no americano casual)"),
        ("U", "iu", ""),
        ("V", "vi", ""),
        ("W", "dãbliu", ""),
        ("X", "éks", ""),
        ("Y", "uai", ""),
        ("Z", "zéd", "no UK/IE diz-se <b>zed</b>, não “zee”"),
    ]
    # tabela em 2 colunas agrupando
    rows_alpha = []
    for letter, sound, note in alphabet:
        note_bit = f" — {note}" if note else ""
        rows_alpha.append((letter, sound, note or "—"))
    story.append(vocab_table(rows_alpha, ("Letra", "Som (aprox.)", "Nota")))
    story.append(Spacer(1, 10))
    story.append(
        TipBox(
            "Atenção britânica",
            "A letra <b>Z</b> se chama <b>zed</b> (não “zee”). Em números de telefone "
            "e soletração isso importa. Ex.: “My name is Zoe — Z-O-E.”",
        )
    )
    story.append(Paragraph("Sons que o português não tem", S["h2"]))
    story.append(
        Paragraph(
            "• <b>th</b> em <i>think</i> /θ/ — língua entre os dentes, ar saindo (surdo).<br/>"
            "• <b>th</b> em <i>this</i> /ð/ — mesma posição, mas com vibração (sonoro).<br/>"
            "• <b>r</b> britânico — na maioria das variedades do sul da Inglaterra, "
            "o R no fim da sílaba quase não se pronuncia: <i>car</i> ≈ “cá”, "
            "<i>water</i> ≈ “uótə”. Na Irlanda, o R costuma ser mais audível.",
            S["body"],
        )
    )
    story.append(Paragraph("Soletrando (spelling aloud)", S["h2"]))
    story.extend(
        phrase_pair(
            "How do you spell that? — J-O-H-N.",
            "Como se soletra isso? — J-O-H-N.",
        )
    )
    story.extend(
        phrase_pair(
            "Could you spell your surname, please?",
            "Pode soletrar o seu sobrenome, por favor?",
        )
    )
    story.append(PageBreak())

    # ========== CAP 2 CUMPRIMENTOS ==========
    story.extend(chapter_header("2", "Cumprimentos e primeiras conversas"))
    story.extend(img("greetings.jpg", width=12 * cm, max_height=9 * cm))
    story.append(
        Paragraph("Cumprimentos no pub britânico e no café irlandês.", S["caption"])
    )
    story.append(Paragraph("Saudações do dia a dia", S["h2"]))
    story.append(
        vocab_table(
            [
                ("Hello / Hi", "helô / rai", "Olá / Oi"),
                ("Good morning", "gúd mórning", "Bom dia (até ~meio-dia)"),
                ("Good afternoon", "gúd áftənun", "Boa tarde"),
                ("Good evening", "gúd ívning", "Boa noite (ao chegar)"),
                ("Good night", "gúd náit", "Boa noite (ao se despedir p/ dormir)"),
                ("How are you?", "hau á iu?", "Como vai?"),
                ("I'm fine, thanks.", "aim fain, fénks", "Estou bem, obrigado/a."),
                ("Nice to meet you.", "nais tu mít iu", "Prazer em conhecê-lo/a."),
                ("See you later.", "sí iu lêitə", "Até mais."),
                ("Bye / Cheerio", "bai / chíriô", "Tchau (cheerio = UK informal)"),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        TipBox(
            "Nota irlandesa [IE]",
            "Na Irlanda é comum ouvir <b>How's the form?</b> ou <b>How's she cutting?</b> "
            "no sentido de “como vai?”. Resposta natural: <b>Grand</b> (= bem / ótimo).",
        )
    )
    story.append(Paragraph("Apresentando-se", S["h2"]))
    story.extend(phrase_pair("What's your name?", "Qual é o seu nome?"))
    story.extend(phrase_pair("My name is Ana. / I'm Ana.", "Meu nome é Ana. / Eu sou a Ana."))
    story.extend(phrase_pair("Where are you from?", "De onde você é?"))
    story.extend(
        phrase_pair(
            "I'm from Brazil. I live in São Paulo.",
            "Sou do Brasil. Mora/vivo em São Paulo.",
        )
    )
    story.extend(phrase_pair("What do you do?", "O que você faz? (profissão)"))
    story.extend(
        phrase_pair(
            "I'm a student. / I work in a café.",
            "Sou estudante. / Trabalho num café.",
        )
    )
    story.append(Paragraph("Diálogo 1 — No café", S["h2"]))
    for line in [
        ("Alex", "Hi! Is this seat free?", "Oi! Este lugar está livre?"),
        ("Sam", "Yes, of course. Please, sit down.", "Sim, claro. Por favor, sente-se."),
        ("Alex", "Thanks. I'm Alex. Nice to meet you.", "Obrigado. Sou Alex. Prazer."),
        ("Sam", "I'm Sam. Are you from around here?", "Sou Sam. Você é daqui?"),
        (
            "Alex",
            "No, I'm from Brazil. I'm here for a week.",
            "Não, sou do Brasil. Estou aqui por uma semana.",
        ),
        (
            "Sam",
            "Lovely! Welcome to Dublin.",
            "Que legal! Bem-vindo/a a Dublin.",
        ),
    ]:
        story.extend(dialogue_line(*line))
    story.append(Paragraph("Palavras de cortesia (essenciais no UK/IE)", S["h2"]))
    story.append(
        vocab_table(
            [
                ("Please", "plíz", "Por favor"),
                ("Thank you / Thanks", "fénk iu / fénks", "Obrigado/a"),
                ("You're welcome", "ió uélkəm", "De nada"),
                ("Excuse me", "ekskiúz mi", "Com licença / Desculpe"),
                ("Sorry", "sóri", "Desculpa"),
                ("Pardon?", "pádən", "Como? (não entendi)"),
            ]
        )
    )
    story.append(PageBreak())

    # ========== CAP 3 NÚMEROS ==========
    story.extend(chapter_header("3", "Números, dias, meses e horas"))
    story.extend(img("numbers-time.jpg", width=11 * cm, max_height=8.5 * cm))
    story.append(Paragraph("Números, calendário e relógio — base de toda conversa.", S["caption"]))
    story.append(Paragraph("Números 0–20", S["h2"]))
    story.append(
        vocab_table(
            [
                ("0 zero", "zíərəu", "zero"),
                ("1 one", "uãn", "um"),
                ("2 two", "tú", "dois"),
                ("3 three", "frí (th)", "três"),
                ("4 four", "fó", "quatro"),
                ("5 five", "faiv", "cinco"),
                ("6 six", "síks", "seis"),
                ("7 seven", "sévən", "sete"),
                ("8 eight", "êit", "oito"),
                ("9 nine", "nain", "nove"),
                ("10 ten", "ten", "dez"),
                ("11 eleven", "ilévən", "onze"),
                ("12 twelve", "tuélv", "doze"),
                ("13 thirteen", "fətín", "treze"),
                ("15 fifteen", "fiftín", "quinze"),
                ("20 twenty", "tuénti", "vinte"),
            ]
        )
    )
    story.append(Paragraph("Dezenas e além", S["h2"]))
    story.append(
        Paragraph(
            "30 thirty · 40 forty · 50 fifty · 60 sixty · 70 seventy · 80 eighty · "
            "90 ninety · 100 a hundred · 1,000 a thousand.<br/>"
            "21 = <b>twenty-one</b> · 45 = <b>forty-five</b> · 108 = <b>a hundred and eight</b> "
            "(no UK/IE usa-se <i>and</i> depois de hundred).",
            S["body"],
        )
    )
    story.append(
        TipBox(
            "Telefone no estilo britânico",
            "O dígito 0 costuma ser lido como <b>oh</b> (não “zero”): "
            "020 7946 0018 → “oh-two-oh, seven-nine-four-six…”.",
        )
    )
    story.append(Paragraph("Dias da semana", S["h2"]))
    story.append(
        vocab_table(
            [
                ("Monday", "mándei", "segunda-feira"),
                ("Tuesday", "tiúzdei", "terça-feira"),
                ("Wednesday", "uênzdei", "quarta-feira"),
                ("Thursday", "fə́zdei", "quinta-feira"),
                ("Friday", "fráidei", "sexta-feira"),
                ("Saturday", "sátədei", "sábado"),
                ("Sunday", "sándei", "domingo"),
            ]
        )
    )
    story.append(
        Paragraph(
            "Dica: os dias são sempre com maiúscula. <i>See you on Monday.</i>",
            S["pt"],
        )
    )
    story.append(Paragraph("Meses", S["h2"]))
    story.append(
        Paragraph(
            "January, February, March, April, May, June, July, August, September, "
            "October, November, December.",
            S["en"],
        )
    )
    story.append(
        Paragraph(
            "Datas no UK/IE: <b>dia / mês / ano</b>. "
            "Ex.: 27/10/2026 = <i>the twenty-seventh of October</i>.",
            S["body"],
        )
    )
    story.append(Paragraph("Que horas são?", S["h2"]))
    story.extend(phrase_pair("What time is it?", "Que horas são?"))
    story.extend(phrase_pair("It's three o'clock.", "São três em ponto."))
    story.extend(phrase_pair("It's half past three. (= 15:30)", "São três e meia."))
    story.extend(phrase_pair("It's quarter past four. (= 16:15)", "São quatro e quinze."))
    story.extend(phrase_pair("It's quarter to five. (= 16:45)", "São quinze para as cinco."))
    story.append(
        TipBox(
            "Estilo britânico clássico",
            "No UK ainda se usa muito <b>half past</b>, <b>quarter past</b> e "
            "<b>quarter to</b>. Também se aceita o formato digital: "
            "<i>It's three thirty.</i>",
        )
    )
    story.append(PageBreak())

    # ========== CAP 4 FAMÍLIA ==========
    story.extend(chapter_header("4", "Família e pessoas"))
    story.extend(img("family.jpg", width=12 * cm, max_height=9 * cm))
    story.append(Paragraph("Vocabulário de família e descrições simples.", S["caption"]))
    story.append(
        vocab_table(
            [
                ("mother / mum", "mãdə / mam", "mãe (mum = UK/IE)"),
                ("father / dad", "fádə / dád", "pai"),
                ("parents", "péərənts", "pais"),
                ("brother / sister", "brãdə / sístə", "irmão / irmã"),
                ("son / daughter", "sãn / dótə", "filho / filha"),
                ("husband / wife", "hãzbənd / uaif", "marido / esposa"),
                ("friend", "frend", "amigo/a"),
                ("neighbour", "nêibə", "vizinho/a (grafia UK: neighbour)"),
                ("child / children", "tchaild / chíldrən", "criança / crianças"),
                ("baby", "bêibi", "bebê"),
            ]
        )
    )
    story.append(Paragraph("Pronomes pessoais", S["h2"]))
    story.append(
        vocab_table(
            [
                ("I", "ai", "eu"),
                ("you", "iu", "você / vocês"),
                ("he / she / it", "hi / shi / it", "ele / ela / isso"),
                ("we", "ui", "nós"),
                ("they", "dêi", "eles / elas"),
            ]
        )
    )
    story.append(Paragraph("Descrevendo alguém", S["h2"]))
    story.extend(phrase_pair("She is tall and friendly.", "Ela é alta e simpática."))
    story.extend(phrase_pair("He has brown hair and blue eyes.", "Ele tem cabelo castanho e olhos azuis."))
    story.extend(phrase_pair("They are my neighbours.", "Eles são meus vizinhos."))
    story.extend(phrase_pair("This is my mum.", "Esta é a minha mãe."))
    story.append(PageBreak())

    # ========== CAP 5 DAILY LIFE ==========
    story.extend(chapter_header("5", "Vida quotidiana (daily life)"))
    story.extend(img("daily-life.jpg", width=12 * cm, max_height=9 * cm))
    story.append(Paragraph("Rotina matinal — vocabulário do dia a dia.", S["caption"]))
    story.append(Paragraph("Verbos de rotina", S["h2"]))
    story.append(
        vocab_table(
            [
                ("wake up", "uêik áp", "acordar"),
                ("get up", "gét áp", "levantar-se"),
                ("have a shower", "hév ə sháuə", "tomar banho (UK: shower)"),
                ("have breakfast", "hév brékfəst", "tomar café da manhã"),
                ("go to work / school", "gôu tu uêrk / skul", "ir ao trabalho / escola"),
                ("have lunch", "hév lântch", "almoçar"),
                ("come home", "kâm hôum", "voltar para casa"),
                ("have dinner", "hév dínə", "jantar"),
                ("watch TV", "uótch ti-ví", "assistir TV"),
                ("go to bed", "gôu tu bed", "ir dormir"),
            ]
        )
    )
    story.append(
        TipBox(
            "UK tip",
            "Em inglês britânico, diz-se <b>have a shower</b> / <b>have a bath</b> "
            "(não “take a shower”, que é mais americano). Também: <b>at the weekend</b> "
            "(US: on the weekend).",
        )
    )
    story.append(Paragraph("Minha rotina — modelo", S["h2"]))
    story.append(
        Paragraph(
            "I wake up at seven o'clock. I have a shower and then I have breakfast — "
            "usually tea and toast. I go to work by bus. I have lunch at one. "
            "I come home at six and have dinner with my family. At the weekend, "
            "I visit my friends.",
            S["en"],
        )
    )
    story.append(
        Paragraph(
            "Acordo às sete. Tomo banho e depois tomo café da manhã — geralmente chá "
            "e torrada. Vou ao trabalho de ônibus. Almoço à uma. Volto para casa às "
            "seis e janto com a família. No fim de semana, visito meus amigos.",
            S["pt"],
        )
    )
    story.append(Paragraph("Meios de transporte", S["h2"]))
    story.append(
        vocab_table(
            [
                ("by bus", "bai bâs", "de ônibus"),
                ("by train", "bai trein", "de trem"),
                ("by Tube / Underground", "tiúb", "de metrô (Londres)"),
                ("on foot", "ón fut", "a pé"),
                ("by bike", "bai baik", "de bicicleta"),
                ("by car", "bai cá", "de carro"),
            ]
        )
    )
    story.append(PageBreak())

    # ========== CAP 6 FOOD ==========
    story.extend(chapter_header("6", "Comida e bebida (UK & Ireland)"))
    story.extend(img("food.jpg", width=12 * cm, max_height=9 * cm))
    story.append(
        Paragraph("Chá, scone, fish & chips, Irish stew, soda bread…", S["caption"])
    )
    story.append(Paragraph("No café / restaurante", S["h2"]))
    story.append(
        vocab_table(
            [
                ("a cup of tea", "ə câp əv tí", "uma xícara de chá"),
                ("a coffee, please", "ə cófi plíz", "um café, por favor"),
                ("Could I have…?", "kud ai hév", "Eu poderia ter…? (educado)"),
                ("the bill, please", "də bil plíz", "a conta, por favor (UK)"),
                ("I'm vegetarian", "aim vejətériən", "Sou vegetariano/a"),
                ("It tastes lovely", "it teists lâvli", "Está delicioso"),
            ]
        )
    )
    story.append(Paragraph("Pratos e comidas típicas", S["h2"]))
    story.append(
        vocab_table(
            [
                ("breakfast", "brékfəst", "café da manhã"),
                ("toast / jam", "tôust / djam", "torrada / geleia"),
                ("scone", "skon / skôun", "scone (bolinho britânico)"),
                ("fish and chips", "fish ən tchips", "peixe com batata frita"),
                ("full English breakfast", "ful ínglish…", "café da manhã completo UK"),
                ("Irish stew", "áirish stiu", "ensopado irlandês"),
                ("soda bread", "sôudə bred", "pão de soda (Irlanda)"),
                ("vegetables", "védjtəblz", "legumes / vegetais"),
                ("fruit", "frut", "fruta"),
                ("water / juice", "uótə / djus", "água / suco"),
            ]
        )
    )
    story.append(
        TipBox(
            "Chá é sério negócio",
            "No UK e na Irlanda, <b>tea</b> não é só a bebida: pode significar a refeição "
            "da tarde/início da noite. “What's for tea?” = “O que tem para o jantar?” "
            "em muitas famílias britânicas e irlandesas.",
        )
    )
    story.append(Paragraph("Diálogo 2 — Pedindo comida", S["h2"]))
    for line in [
        ("Waiter", "Hiya! What can I get you?", "Oi! O que posso trazer?"),
        (
            "You",
            "Could I have a pot of tea and a scone, please?",
            "Poderia me trazer um bule de chá e um scone, por favor?",
        ),
        ("Waiter", "Of course. Anything else?", "Claro. Mais alguma coisa?"),
        (
            "You",
            "No, that's all. Thanks.",
            "Não, só isso. Obrigado/a.",
        ),
    ]:
        story.extend(dialogue_line(*line))
    story.append(PageBreak())

    # ========== CAP 7 GRAMMAR ==========
    story.extend(chapter_header("7", "Gramática essencial do iniciante"))
    story.extend(img("grammar.jpg", width=11 * cm, max_height=8 * cm))
    story.append(Paragraph("Quadro, caderno e os tijolos da língua.", S["caption"]))
    story.append(
        Paragraph(
            "Não tente decorar 50 regras. Domine estes quatro blocos e você já "
            "consegue se comunicar no dia a dia.",
            S["body"],
        )
    )
    story.append(Paragraph("1) O verbo TO BE (ser / estar)", S["h2"]))
    story.append(
        vocab_table(
            [
                ("I am (I'm)", "ai ém", "eu sou / estou"),
                ("you are (you're)", "iu á", "você é / está"),
                ("he/she/it is (he's…)", "hiz / shiz / its", "ele/ela é / está"),
                ("we are (we're)", "ui á", "nós somos / estamos"),
                ("they are (they're)", "dêi á", "eles são / estão"),
            ]
        )
    )
    story.append(Paragraph("Negativa: I'm not / you aren't / he isn't…", S["body_left"]))
    story.append(Paragraph("Pergunta: Are you…? Is she…? — Yes, I am. / No, I'm not.", S["body_left"]))
    story.append(Paragraph("2) Present Simple (hábitos)", S["h2"]))
    story.append(
        Paragraph(
            "Uso: rotinas e fatos. Na 3ª pessoa (he/she/it), o verbo ganha <b>-s</b>:<br/>"
            "I work → he work<b>s</b> · I go → she goe<b>s</b> · I study → he studie<b>s</b>.",
            S["body"],
        )
    )
    story.extend(phrase_pair("I live in Cork.", "Eu moro em Cork."))
    story.extend(phrase_pair("She works in a bookshop.", "Ela trabalha numa livraria."))
    story.extend(phrase_pair("Do you speak English?", "Você fala inglês?"))
    story.extend(phrase_pair("I don't speak Irish yet.", "Ainda não falo irlandês (gaélico)."))
    story.append(Paragraph("3) Artigos: a / an / the", S["h2"]))
    story.append(
        Paragraph(
            "• <b>a</b> + som consonantal: a book, a university (som de “iú”).<br/>"
            "• <b>an</b> + som vocálico: an apple, an hour (h mudo).<br/>"
            "• <b>the</b> = o/a específico(a): the bus to Dublin.",
            S["body"],
        )
    )
    story.append(Paragraph("4) There is / There are", S["h2"]))
    story.extend(phrase_pair("There is a park near my house.", "Há um parque perto da minha casa."))
    story.extend(phrase_pair("There are two cafés on this street.", "Há dois cafés nesta rua."))
    story.append(Paragraph("5) Perguntas com Wh-", S["h2"]))
    story.append(
        vocab_table(
            [
                ("What…?", "uót", "O que / Qual?"),
                ("Where…?", "uéə", "Onde?"),
                ("When…?", "uén", "Quando?"),
                ("Who…?", "hu", "Quem?"),
                ("Why…?", "uai", "Por quê?"),
                ("How…?", "hau", "Como?"),
                ("How much / How many?", "hau mâtch / méni", "Quanto(s)?"),
            ]
        )
    )
    story.append(PageBreak())

    # ========== CAP 8 LUGARES ==========
    story.extend(chapter_header("8", "Lugares, direções e viagem"))
    story.append(
        vocab_table(
            [
                ("street / road", "strit / rôud", "rua / estrada"),
                ("city centre", "síti séntə", "centro da cidade (UK spelling)"),
                ("train station", "trein stêishən", "estação de trem"),
                ("airport", "éəport", "aeroporto"),
                ("hotel / hostel", "houtél / hóstəl", "hotel / hostel"),
                ("museum", "miuzíəm", "museu"),
                ("park", "pak", "parque"),
                ("shop", "shop", "loja (US: store)"),
                ("chemist", "kémist", "farmácia (UK; US: pharmacy)"),
                ("toilet / loo", "tóilət / lu", "banheiro (loo = informal UK)"),
            ]
        )
    )
    story.append(Paragraph("Pedindo informação", S["h2"]))
    story.extend(phrase_pair("Excuse me, where is the station?", "Com licença, onde fica a estação?"))
    story.extend(phrase_pair("How do I get to the museum?", "Como chego ao museu?"))
    story.extend(phrase_pair("Turn left / Turn right.", "Vire à esquerda / à direita."))
    story.extend(phrase_pair("Go straight on.", "Siga em frente."))
    story.extend(phrase_pair("It's next to the bank.", "Fica ao lado do banco."))
    story.extend(phrase_pair("It's opposite the park.", "Fica em frente ao parque."))
    story.append(
        TipBox(
            "No ônibus e no trem",
            "“A single to Bath, please.” = ida simples. "
            "“A return to Bath, please.” = ida e volta (UK). "
            "Na Irlanda: “A return to Galway, please.” também é natural.",
        )
    )
    story.append(PageBreak())

    # ========== CAP 9 IRISH ENGLISH ==========
    story.extend(chapter_header("9", "Inglês irlandês: o que notar"))
    story.append(
        Paragraph(
            "O inglês falado na Irlanda (Hiberno-English) é inglês de verdade — "
            "não é “errado”. Tem influência do irlandês (Gaeilge) na melodia e "
            "em algumas estruturas. Você será compreendido com o inglês britânico "
            "padrão; estas notas ajudam a <b>entender</b> melhor os locais.",
            S["body"],
        )
    )
    story.append(Paragraph("Palavras e expressões [IE]", S["h2"]))
    story.append(
        vocab_table(
            [
                ("grand", "grand", "bem / ótimo / tudo certo"),
                ("what's the story?", "uóts də stóri", "e aí? / como vão as coisas?"),
                ("I'm wrecked", "aim rékt", "estou destruído/a (cansado)"),
                ("a cuppa", "ə câpə", "uma xícara de chá"),
                ("the jacks", "də djacs", "o banheiro (informal)"),
                ("give us a shout", "giv əs ə shaut", "me liga / me avisa"),
                ("ye", "ii", "vocês (plural informal)"),
                ("fierce", "fíəs", "muito (ex.: fierce cold)"),
            ]
        )
    )
    story.append(Paragraph("Construções típicas", S["h2"]))
    story.extend(
        phrase_pair(
            "I'm after eating.  [= I have just eaten]",
            "Acabei de comer. (estrutura clássica do Hiberno-English)",
        )
    )
    story.extend(
        phrase_pair(
            "Will I open the window?  [= Shall I…?]",
            "Quer que eu abra a janela? (will I… muito comum na Irlanda)",
        )
    )
    story.extend(
        phrase_pair(
            "He's brilliant so he is.",
            "Ele é demais — reforço enfático no fim da frase.",
        )
    )
    story.append(
        TipBox(
            "Cortesia irlandesa",
            "Irlandeses costumam ser calorosos e indiretos. Um “sorry” ou "
            "“thanks a million” aparece com frequência. Responder com um sorriso "
            "e “no bother” (= sem problema) soa natural.",
        )
    )
    story.append(PageBreak())

    # ========== CAP 10 UK vs US ==========
    story.extend(chapter_header("10", "Britânico × Americano (diferenças úteis)"))
    story.append(
        Paragraph(
            "Os dois são corretos. Este livro prioriza o britânico/irlandês. "
            "Conhecer as diferenças evita confusão em filmes, apps e viagens.",
            S["body"],
        )
    )
    story.append(
        vocab_table(
            [
                ("flat", "apartment", "apartamento"),
                ("lift", "elevator", "elevador"),
                ("lorry", "truck", "caminhão"),
                ("biscuit", "cookie", "biscoito"),
                ("crisps", "chips", "salgadinho de batata"),
                ("chips", "fries", "batata frita"),
                ("holiday", "vacation", "férias"),
                ("queue", "line", "fila"),
                ("trousers", "pants", "calças"),
                ("rubber", "eraser", "borracha (cuidado: pants/rubber mudam de sentido!)"),
                ("colour / favour", "color / favor", "grafia -our (UK) vs -or (US)"),
                ("centre / theatre", "center / theater", "grafia -re (UK) vs -er (US)"),
            ],
            ("UK / Ireland", "United States", "Significado"),
        )
    )
    story.append(PageBreak())

    # ========== CAP 11 DIÁLOGOS ==========
    story.extend(chapter_header("11", "Diálogos para praticar"))
    story.append(
        Paragraph(
            "Leia em voz alta duas vezes: primeiro olhando a tradução, depois "
            "escondendo o português.",
            S["body"],
        )
    )
    story.append(Paragraph("Diálogo A — No aeroporto", S["h2"]))
    for line in [
        ("Officer", "Good morning. Passport, please.", "Bom dia. Passaporte, por favor."),
        ("You", "Here you are.", "Aqui está."),
        ("Officer", "What's the purpose of your visit?", "Qual o motivo da sua visita?"),
        ("You", "I'm here on holiday.", "Estou aqui de férias."),
        ("Officer", "How long are you staying?", "Quanto tempo vai ficar?"),
        ("You", "Ten days.", "Dez dias."),
        ("Officer", "Enjoy your stay.", "Aproveite a estadia."),
    ]:
        story.extend(dialogue_line(*line))

    story.append(Paragraph("Diálogo B — Pedindo direções em Londres", S["h2"]))
    for line in [
        ("You", "Excuse me, how do I get to the British Museum?", "Com licença, como chego ao British Museum?"),
        (
            "Local",
            "Take the Tube to Russell Square and then walk. It's about five minutes.",
            "Pegue o metrô até Russell Square e depois ande. São uns cinco minutos.",
        ),
        ("You", "Is it far from here?", "É longe daqui?"),
        ("Local", "Not really. Ten minutes on the Tube.", "Na verdade não. Dez minutos de metrô."),
        ("You", "Thanks a lot!", "Muito obrigado/a!"),
        ("Local", "You're welcome. Have a nice day!", "De nada. Tenha um ótimo dia!"),
    ]:
        story.extend(dialogue_line(*line))

    story.append(Paragraph("Diálogo C — Em Dublin, pedindo um chá", S["h2"]))
    for line in [
        ("Barista", "Hiya, what's the story? What can I get you?", "E aí? O que vai querer?"),
        ("You", "A cuppa and a slice of soda bread, please.", "Um chá e uma fatia de soda bread, por favor."),
        ("Barista", "Grand. Eat in or take away?", "Perfeito. Aqui ou para viagem?"),
        ("You", "Eat in, please.", "Aqui, por favor."),
        ("Barista", "Lovely. It'll be ready in a minute.", "Ótimo. Fica pronto num minutinho."),
    ]:
        story.extend(dialogue_line(*line))
    story.append(PageBreak())

    # ========== CAP 12 EXERCÍCIOS ==========
    story.extend(chapter_header("12", "Exercícios + respostas"))
    story.append(Paragraph("A) Complete com to be (am / is / are)", S["h2"]))
    for i, q in enumerate(
        [
            "I _____ from Brazil.",
            "She _____ my sister.",
            "We _____ in London.",
            "_____ you a student?",
            "They _____ not at home.",
        ],
        1,
    ):
        story.append(Paragraph(f"{i}. {q}", S["exercise"]))

    story.append(Paragraph("B) Traduza para o inglês britânico", S["h2"]))
    for i, q in enumerate(
        [
            "Bom dia! Como vai?",
            "Meu nome é Carla. Prazer em conhecê-lo.",
            "Que horas são? São duas e meia.",
            "Onde fica a estação de trem?",
            "Eu poderia ter um chá, por favor?",
            "No fim de semana eu visito meus pais.",
        ],
        1,
    ):
        story.append(Paragraph(f"{i}. {q}", S["exercise"]))

    story.append(Paragraph("C) UK ou US? Circule a forma britânica", S["h2"]))
    for i, q in enumerate(
        [
            "flat / apartment",
            "elevator / lift",
            "colour / color",
            "chips (batata frita) / fries",
            "zed / zee (nome da letra Z)",
        ],
        1,
    ):
        story.append(Paragraph(f"{i}. {q}", S["exercise"]))

    story.append(Paragraph("D) Responda sobre você (frases curtas)", S["h2"]))
    for i, q in enumerate(
        [
            "What's your name?",
            "Where are you from?",
            "What do you do?",
            "What time do you wake up?",
            "What do you have for breakfast?",
        ],
        1,
    ):
        story.append(Paragraph(f"{i}. {q}", S["exercise"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Respostas", S["h2"]))
    story.append(AccentBar())
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>A)</b> 1. am  2. is  3. are  4. Are  5. are", S["body_left"]))
    story.append(
        Paragraph(
            "<b>B)</b> 1. Good morning! How are you?  "
            "2. My name is Carla. Nice to meet you.  "
            "3. What time is it? It's half past two.  "
            "4. Where is the train station?  "
            "5. Could I have a tea, please?  "
            "6. At the weekend I visit my parents.",
            S["body_left"],
        )
    )
    story.append(
        Paragraph(
            "<b>C)</b> 1. flat  2. lift  3. colour  4. chips  5. zed",
            S["body_left"],
        )
    )
    story.append(
        Paragraph(
            "<b>D)</b> Respostas pessoais. Exemplos: "
            "My name is João. I'm from Recife. I'm a student. "
            "I wake up at seven. I have coffee and bread.",
            S["body_left"],
        )
    )
    story.append(PageBreak())

    # ========== GLOSSÁRIO ==========
    story.append(Paragraph("Glossário rápido A–Z", S["h1"]))
    story.append(AccentBar())
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Uma seleção das palavras mais úteis deste ebook. Volte aqui sempre "
            "que esquecer um termo.",
            S["body"],
        )
    )
    glossary = [
        ("again", "de novo"),
        ("always", "sempre"),
        ("and", "e"),
        ("because", "porque"),
        ("before / after", "antes / depois"),
        ("big / small", "grande / pequeno"),
        ("book", "livro"),
        ("but", "mas"),
        ("buy / sell", "comprar / vender"),
        ("cheap / expensive", "barato / caro"),
        ("clean / dirty", "limpo / sujo"),
        ("cold / hot", "frio / quente"),
        ("come / go", "vir / ir"),
        ("day / night", "dia / noite"),
        ("early / late", "cedo / tarde"),
        ("easy / difficult", "fácil / difícil"),
        ("eat / drink", "comer / beber"),
        ("every day", "todo dia"),
        ("family", "família"),
        ("food", "comida"),
        ("friend", "amigo/a"),
        ("good / bad", "bom / ruim"),
        ("happy / sad", "feliz / triste"),
        ("here / there", "aqui / ali"),
        ("house / home", "casa / lar"),
        ("I don't know", "eu não sei"),
        ("important", "importante"),
        ("job / work", "emprego / trabalho"),
        ("language", "idioma"),
        ("learn / teach", "aprender / ensinar"),
        ("left / right", "esquerda / direita"),
        ("like / love", "gostar / amar"),
        ("listen / speak", "ouvir / falar"),
        ("little / a lot", "pouco / muito"),
        ("maybe", "talvez"),
        ("money", "dinheiro"),
        ("month / year", "mês / ano"),
        ("morning", "manhã"),
        ("near / far", "perto / longe"),
        ("need", "precisar"),
        ("never / sometimes", "nunca / às vezes"),
        ("new / old", "novo / velho"),
        ("next", "próximo"),
        ("now / today", "agora / hoje"),
        ("open / close", "abrir / fechar"),
        ("people", "pessoas"),
        ("phone", "telefone"),
        ("please", "por favor"),
        ("question / answer", "pergunta / resposta"),
        ("read / write", "ler / escrever"),
        ("really", "realmente"),
        ("right (correct)", "certo"),
        ("same / different", "igual / diferente"),
        ("school", "escola"),
        ("see", "ver"),
        ("shop", "loja / fazer compras"),
        ("sorry", "desculpa"),
        ("start / finish", "começar / terminar"),
        ("stop", "parar"),
        ("street", "rua"),
        ("sure", "claro / certeza"),
        ("talk / tell", "conversar / contar"),
        ("thank you", "obrigado/a"),
        ("think", "pensar"),
        ("time", "tempo / hora"),
        ("today / tomorrow / yesterday", "hoje / amanhã / ontem"),
        ("too", "também / demais"),
        ("town / city", "cidade pequena / cidade"),
        ("understand", "entender"),
        ("very", "muito"),
        ("wait", "esperar"),
        ("want", "querer"),
        ("water", "água"),
        ("weather", "clima / tempo"),
        ("week / weekend", "semana / fim de semana"),
        ("well", "bem"),
        ("with / without", "com / sem"),
        ("word", "palavra"),
        ("yes / no", "sim / não"),
    ]
    # render in two-column table chunks
    mid = (len(glossary) + 1) // 2
    left, right = glossary[:mid], glossary[mid:]
    while len(right) < len(left):
        right.append(("", ""))
    data = [[Paragraph("<b>English</b>", S["cell_head"]),
             Paragraph("<b>Português</b>", S["cell_head"]),
             Paragraph("<b>English</b>", S["cell_head"]),
             Paragraph("<b>Português</b>", S["cell_head"])]]
    for (e1, p1), (e2, p2) in zip(left, right):
        data.append(
            [
                Paragraph(e1, S["cell_b"]),
                Paragraph(p1, S["cell"]),
                Paragraph(e2, S["cell_b"]),
                Paragraph(p2, S["cell"]),
            ]
        )
    gtable = Table(data, colWidths=[4 * cm, 3.8 * cm, 4 * cm, 3.8 * cm])
    gtable.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), FOREST),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [IVORY, MIST]),
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(gtable)
    story.append(PageBreak())

    # ========== ENCERRAMENTO ==========
    story.append(Paragraph("Próximos passos", S["h1"]))
    story.append(AccentBar())
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Você terminou o mapa do iniciante. Para continuar evoluindo no inglês "
            "britânico e irlandês:",
            S["body"],
        )
    )
    for tip in [
        "<b>Ouça.</b> BBC Learning English, podcasts irlandeses (ex.: conversas "
        "leves do RTÉ) e séries britânicas com legendas em inglês.",
        "<b>Fale.</b> Grave-se lendo os diálogos deste livro. Compare no dia seguinte.",
        "<b>Escreva.</b> Cinco frases por dia sobre a sua rotina, no Present Simple.",
        "<b>Anote.</b> Um caderno só de “frases úteis” vale mais do que listas "
        "gigantes de palavras soltas.",
        "<b>Seja gentil consigo.</b> Errar faz parte. Locais no UK e na Irlanda "
        "costumam ajudar quem está aprendendo.",
    ]:
        story.append(Paragraph(tip, S["body_left"]))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 16))
    story.append(
        TipBox(
            "Frase para levar na bagagem",
            "“I'm learning English — could you speak a little more slowly, please?” "
            "Essa frase sozinha destrava metade das conversas reais.",
        )
    )
    story.append(Spacer(1, 28))
    story.append(Paragraph("Go n-éirí an bóthar leat.", S["cover_sub"]))
    story.append(
        Paragraph(
            "(Irlandês: “Que o caminho se erga ao seu encontro” — boa sorte na jornada.)",
            S["caption"],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("English from These Isles", S["en"]))
    story.append(
        Paragraph(
            "Inglês Britânico & Irlandês para Iniciantes  ·  Nível A1–A2",
            S["small"],
        )
    )

    doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
    print(f"PDF gerado: {OUT}")
    print(f"Tamanho: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
