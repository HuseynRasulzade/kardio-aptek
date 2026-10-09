#!/usr/bin/env python3
"""Static site generator for Kardio Aptek. Run: python3 build.py  -> writes *.html next to this file."""
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "Kardio Aptek"
PHONE_RAW = "+994502779434"
PHONE_SHOW = "+994 50 277 94 34"
WA = PHONE_RAW.lstrip("+")
YEAR = 2024
HOURS = "Hər gün 09:00 – 22:00"
MAPQ = "Qara Qarayev metrostansiyası, S. Mirzəyev küçəsi, Bakı, Azerbaijan"
MAP_EMBED = "https://maps.google.com/maps?q=" + MAPQ.replace(" ", "+") + "&z=16&output=embed&hl=az"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=" + MAPQ.replace(" ", "+")
MAP_DIR = "https://www.google.com/maps/dir/?api=1&destination=" + MAPQ.replace(" ", "+")
CITY = "Qara Qarayev metrostansiyası yaxınlığı, S. Mirzəyev küçəsi, Bakı, AZ1002, Azərbaycan"

LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#0f766e"/>'
        '<path d="M24 38S9 29.5 9 19.2C9 14.6 12.4 11 16.7 11c3 0 5.6 1.7 7.3 4.3C25.700 12.700 28.300 11 31.300 11 35.600 11 39 14.600 39 19.200 39 29.500 24 38 24 38Z" fill="#fff"/>'
        '<path d="M12 23h7l2.500-5 4 10 2.500-5H36" fill="none" stroke="#d92d45" stroke-width="2.600" stroke-linecap="round" stroke-linejoin="round"/></svg>')

ICON = {
    "pill": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5-7-7a4.950 4.950 0 0 1 7-7l7 7a4.950 4.950 0 0 1-7 7Z"/><path d="m8.500 8.500 7 7"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.920v3a2 2 0 0 1-2.180 2 19.790 19.790 0 0 1-8.630-3.070 19.500 19.500 0 0 1-6-6A19.790 19.790 0 0 1 2.120 4.180 2 2 0 0 1 4.110 2h3a2 2 0 0 1 2 1.720c.130.960.360 1.900.700 2.810a2 2 0 0 1-.450 2.110L8.090 9.910a16 16 0 0 0 6 6l1.270-1.270a2 2 0 0 1 2.110-.450c.910.340 1.850.570 2.810.700A2 2 0 0 1 22 16.920Z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.840 4.610a5.500 5.500 0 0 0-7.780 0L12 5.670l-1.060-1.060a5.500 5.500 0 0 0-7.780 7.780l1.060 1.060L12 21.230l7.780-7.780 1.060-1.060a5.500 5.500 0 0 0 0-7.780Z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.500A2.500 2.500 0 0 1 6.500 17H20V3H6.500A2.500 2.500 0 0 0 4 5.500v14Z"/><path d="M20 17v4H6.500A2.500 2.500 0 0 1 4 18.500"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.500 14.400c-.300-.150-1.750-.860-2-.960-.270-.100-.470-.150-.670.150-.200.300-.770.960-.940 1.160-.170.200-.350.220-.650.070a8.100 8.100 0 0 1-2.400-1.480 9 9 0 0 1-1.660-2.070c-.170-.300 0-.460.130-.610.130-.130.300-.350.450-.520.150-.170.200-.300.300-.500.100-.200.050-.370-.020-.520-.080-.150-.670-1.620-.920-2.220-.240-.580-.490-.500-.670-.510h-.570c-.200 0-.520.080-.800.370-.270.300-1.040 1.020-1.040 2.480s1.070 2.880 1.220 3.080c.150.200 2.100 3.200 5.080 4.490.710.300 1.260.490 1.700.630.710.230 1.360.200 1.870.120.570-.080 1.750-.720 2-1.410.250-.700.250-1.290.170-1.410-.070-.130-.270-.200-.570-.350ZM12 2a10 10 0 0 0-8.600 15.100L2 22l5.050-1.320A10 10 0 1 0 12 2Z"/></svg>',
    "ecg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.200" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 4 10 2-5h6"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.700s7 7.200 7 12a7 7 0 0 1-14 0c0-4.800 7-12 7-12Z"/></svg>',
}

NAV = [
    ("index.html", "Ana səhifə"),
    ("haqqimizda.html", "Haqqımızda"),
    ("dermanlar.html", "Dərmanlar"),
    ("xidmetler.html", "Xidmətlər"),
    ("meslehetler.html", "Məsləhətlər"),
    ("suallar.html", "Suallar"),
    ("elaqe.html", "Əlaqə"),
]

# --------------------------------------------------------------------------- products
PRODUCTS = [
    dict(
        slug="karno-mer", name="Karno Mer", cat="urek", kind="BAQM", kindcls="",
        short="Ürək-damar sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
        form="Kapsul", pack="30 kapsul (2×15 blister), karton qutu",
        card="karno-card.jpg", head="karno-qutu.jpg",
        comp_title="1 kapsulun tərkibi",
        ing=[("L-karnitin", "L-carnitine", "500 mq"), ("Koenzim Q10", "Coenzyme Q10", "40 mq"), ("Kuersetin", "Quercetin", "25 mq")],
        excip="Mikrokristallik sellüloza, maqnezium stearat, jelatin, oliqofruktoza, nişasta.",
        indication="Ürək-damar sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
        dose=["Böyüklər: 1 kapsul gündə 1 dəfə daxilə qəbul edilir.", "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər."],
        contra=["Məhsulun tərkibindəki hər hansı komponentə qarşı fərdi həssaslıq."],
        storage="25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə.",
        shelf="3 il. Yararlılıq müddəti bitdikdən sonra qəbul etmək olmaz.",
        mfr="FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
        series="FTL/1246", made="10.2024", exp="10.2027", reg="01-Q-00589", extra="QOST/ГОСТ 23058-89", rx="Reseptsiz",
        gallery=[("karno-qutu.jpg", "Karno Mer — qutunun ön üzü"), ("karno-terkib.jpg", "Tərkib və istifadə qaydası"),
                 ("karno-vereq.jpg", "İstifadə təlimatı vərəqi"), ("karno-istehsalci.jpg", "İstehsalçı və sertifikatlar"),
                 ("karno-tarix.jpg", "Seriya, istehsal və son istifadə tarixi")],
    ),
    dict(
        slug="depomer-d3-k2", name="Depomer D3+K2", cat="vitamin", kind="BAQM", kindcls="",
        short="D3 və K2 vitaminlərinin əlavə mənbəyi — 15 ml damcı məhlul (50 000 BV).",
        form="Daxilə qəbul üçün məhlul-damcı", pack="15 ml şüşə flakon, karton qutu (1 ml = 25 damcı)",
        card="depomer-card.jpg", head="depomer-qutu.jpg",
        comp_title="15 ml-in tərkibi (1 ml = 25 damcı)",
        ing=[("Vitamin D3", "Cholecalciferol", "50 000 BV"), ("Vitamin K2", "Menaquinone", "200 mkq")],
        excip="Zeytun yağı.",
        indication="D3 və K2 vitaminlərinin əlavə mənbəyi kimi tövsiyə olunan vasitə.",
        dose=["2–4 yaş arası uşaqlar: 1 damcı gündə 1 dəfə.", "4–14 yaş arası uşaqlar: 2 damcı gündə 1 dəfə.",
              "14 yaşdan yuxarı uşaqlar və böyüklər: 4 damcı gündə 1 dəfə.",
              "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər.", "İstifadədən əvvəl flakonu çalxalayın."],
        contra=["Tərkibindəki hər hansı inqrediyentə qarşı fərdi həssaslıq.", "D hipervitaminozu, hiperkalsiemiya, hiperkalsiuriya.",
                "Böyrək çatmazlığı, böyrək daşları xəstəliyi.", "Ağciyər vərəminin aktiv forması."],
        storage="25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə.",
        shelf="3 il. Yararlılıq müddəti bitdikdən sonra qəbul etmək olmaz.",
        mfr="FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
        series="DK1012", made="02.2026", exp="02.2029", reg="01-Q-00589", extra="AQTA qeydiyyat № MQ-05-001738 · TŞ AZ 1006595881.003-2022", rx="Reseptsiz",
        gallery=[("depomer-qutu.jpg", "Depomer D3+K2 — qutunun ön üzü"), ("depomer-terkib.jpg", "Tərkib və doza (Azərbaycan dilində)"),
                 ("depomer-terkib-en.jpg", "Composition and dosage (English)"), ("depomer-vereq.jpg", "İstifadə təlimatı vərəqi")],
    ),
    dict(
        slug="revimer", name="Revimer", cat="immun", kind="BAQM", kindcls="",
        short="İmmun sistemin fəaliyyətini yaxşılaşdırmaq məqsədilə — 10 flakon × 15 ml məhlul.",
        form="Daxilə qəbul üçün məhlul", pack="15 ml şüşə flakon, No.10, karton qutu",
        card="revimer-card.jpg", head="revimer-qutu.jpg",
        comp_title="15 ml-in tərkibi",
        ing=[("Arı südü tozu, liofilizə olunmuş", "Royal jelly lyophilized powder", "200 mq"),
             ("Barbados albalısı meyvə ekstraktı tozu", "Malpighia emarginata", "150 mq"),
             ("Qaragilə meyvə konsentratı", "Vaccinium myrtillus", "750 mq"),
             ("Qara kəndələş meyvə konsentratı", "Sambucus nigra", "500 mq"),
             ("Böyürtkən meyvə ekstraktı", "Rubus fruticosus", "375 mq")],
        excip="Deionizə olunmuş su, ksantan qətranı, limon turşusu, moruq aroması, kalium sorbat, natrium benzoat, sukraloza.",
        indication="İmmun sistemin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
        dose=["Böyüklər: 15 ml gündə 1 dəfə.", "Digər hallarda həkim məsləhəti ilə tövsiyə oluna bilər.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
        contra=["Məhsulun tərkibindəki hər hansı komponentə qarşı həssaslıq."],
        storage="25 °C-dən yüksək olmayan temperaturda, quru və uşaqların əli çatmayan yerdə.",
        shelf="3 il.",
        mfr="EVA MED MMC (Azərbaycan Respublikası, Bakı)", brand="EVA MED Medicine",
        series="116", made="05.01.2026", exp="05.01.2029", reg="", extra="", rx="Reseptsiz",
        gallery=[("revimer-qutu.jpg", "Revimer — qutunun ön üzü"), ("revimer-terkib.jpg", "Tərkib, köməkçi maddələr və doza"),
                 ("revimer-vereq.jpg", "İstifadə təlimatı vərəqi (1)"), ("revimer-vereq2.jpg", "İstifadə təlimatı vərəqi (2)"),
                 ("revimer-istehsalci.jpg", "İstehsalçı və saxlanma şəraiti"), ("revimer-tarix.jpg", "İstehsal və son istifadə tarixi")],
    ),
    dict(
        slug="chondramer", name="Chondramer", cat="oynaq", kind="Tibbi vasitə", kindcls="red",
        short="Oynaq və əzələ ağrıları üçün istifadə olunan gel — 75 q.",
        form="Yerli istifadə üçün gel", pack="75 q plastik tubik, karton qutu",
        card="chondramer-card.jpg", head="chondramer-qutu.jpg",
        comp_title="75 q gel-in tərkibi",
        ing=[("Glukozamin sulfat", "Glucosamine sulphate", "800 mq"), ("Xondroitin sulfat", "Chondroitin sulphate", "200 mq"),
             ("Metilsulfonilmetan", "Methylsulphonylmethane", "200 mq"), ("Bosvelliya ekstraktı", "Boswellia serrata extract", "120 mq"),
             ("Evkalipt yağı", "Eucalyptus oil", "50 mq"), ("Kəklikotu yağı", "Thyme oil", "10 mq"), ("Mixək yağı", "Clove oil", "5 mq"),
             ("Rozmarin yağı", "Rosemary oil", "12 mq"), ("Kamfora", "Camphor", "20 mq"), ("Mentol", "Menthol", "150 mq")],
        excip="Aromaterapiya yağları (zəncəfil, lavanda, zirə, qoz, portağal yağı), qliserin, karbomer.",
        indication="Oynaq və əzələ ağrıları üçün istifadə olunan tibbi vasitə.",
        dose=["Yerli və xaricdən tətbiq edin. Birbaşa oynaqların və əzələlərin nahiyəsinə masaj edərək sürtün.",
              "İstənilən effekti əldə etmək üçün təmizlənmiş dəri nahiyəsinə gündə ən azı 2–3 dəfə yerli olaraq istifadə edilməlidir.",
              "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər."],
        contra=["Tərkibində olan hər hansı komponentə qarşı fərdi həssaslıq."],
        storage="25 °C-dən yüksək olmayan temperaturda, quru, işıq düşməyən və uşaqların əli çatmayan yerdə.",
        shelf="3 il. İstifadə müddəti bitdikdən sonra istifadə etməyin.",
        mfr="FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
        series="CM1011", made="02.2025", exp="02.2028", reg="", extra="", rx="Reseptsiz",
        gallery=[("chondramer-qutu.jpg", "Chondramer — qutunun ön üzü"), ("chondramer-terkib.jpg", "Tərkib və istifadə qaydası"),
                 ("chondramer-vereq.jpg", "İstifadə təlimatı vərəqi"), ("chondramer-istehsalci.jpg", "İstehsalçı, seriya və tarixlər")],
    ),
]
CATS = [("all", "Hamısı"), ("urek", "Ürək-damar"), ("vitamin", "Vitaminlər"), ("immun", "İmmunitet"), ("oynaq", "Oynaq və əzələ")]

# --------------------------------------------------------------------------- layout
def head(title, desc, extra=""):
    full = f"{title} | {SITE}" if title != SITE else f"{SITE} — Sağlamlığınız üçün etibarlı ünvan"
    return f"""<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0f766e">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="az_AZ">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap&subset=latin-ext" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra}
</head>"""


CUR = ' aria-current="page"'
PHONE_ICON = ICON["phone"].replace("<svg", '<svg width="16" height="16"')


def header(active):
    links = "".join(
        f'<li><a href="{h}"{CUR if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f"""<body>
<a class="skip" href="#main">Əsas məzmuna keç</a>
<header class="site"><div class="container">
<a class="logo" href="index.html" aria-label="{SITE} — ana səhifə">{LOGO}<span>Kardio <b>Aptek</b></span></a>
<nav class="main" id="nav" aria-label="Əsas menyu"><ul>{links}</ul></nav>
<div class="header-cta"><a class="btn btn-primary btn-sm" href="tel:{PHONE_RAW}">{PHONE_ICON} Zəng et</a>
<button class="menu-btn" aria-label="Menyu" aria-expanded="false" aria-controls="nav" type="button">☰</button></div>
</div></header>
<main id="main">"""


def footer():
    fl = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    pl = "".join(f'<li><a href="derman-{p["slug"]}.html">{p["name"]}</a></li>' for p in PRODUCTS)
    return f"""</main>
<footer class="site"><div class="container">
<div class="cols">
<div><a class="logo" href="index.html">{LOGO}<span>Kardio Aptek</span></a>
<p style="margin-top:14px">Ürək sağlamlığı və gündəlik rifahınız üçün keyfiyyətli məhsullar, peşəkar məsləhət və səmimi xidmət.</p></div>
<div><h4>Səhifələr</h4><ul>{fl}</ul></div>
<div><h4>Məhsullar</h4><ul>{pl}<li><a href="dermanlar.html">Bütün məhsullar →</a></li></ul></div>
<div><h4>Əlaqə</h4><ul>
<li>📞 <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></li>
<li>💬 <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
<li>🕘 {HOURS}</li>
<li>📍 <a href="{MAP_LINK}" target="_blank" rel="noopener">{CITY}</a></li>
<li><a href="mexfiyyet.html">Məxfilik siyasəti</a></li></ul></div>
</div>
<div class="legal"><span>© {YEAR} Kardio Aptek. Bütün hüquqlar qorunur.</span>
<span>Saytdakı məlumatlar məlumat xarakterlidir və həkim məsləhətini əvəz etmir.</span></div>
</div></footer>
<div class="fab"><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON['wa']}</a>
<a class="tel" href="tel:{PHONE_RAW}" aria-label="Zəng et">{ICON['phone']}</a></div>
<script src="assets/js/main.js" defer></script>
</body></html>"""


def page_hero(title, sub, crumbs=None):
    c = ""
    if crumbs:
        c = '<div class="crumbs"><a href="index.html">Ana səhifə</a> / ' + " / ".join(crumbs) + "</div>"
    return f'<section class="page-hero"><div class="container">{c}<h1>{title}</h1><p>{sub}</p></div></section>'


def cta_block():
    return f"""<section class="section"><div class="container"><div class="cta reveal">
<div><h2>Sualınız var? Bizə zəng edin</h2><p>Əczaçılarımız məhsullar barədə məlumat verməyə hazırdır.</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="tel:{PHONE_RAW}">📞 {PHONE_SHOW}</a>
<a class="btn btn-outline" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></div></div></div></section>"""


def product_card(p):
    return f"""<article class="card product reveal" data-cat="{p['cat']}">
<a class="thumb" href="derman-{p['slug']}.html" aria-label="{p['name']}"><img src="assets/img/{p['card']}" alt="{p['name']} qutusu" loading="lazy"></a>
<div class="body"><span class="tag {p['kindcls']}">{p['kind']}</span><h3>{p['name']}</h3><p class="sub">{p['short']}</p>
<div class="actions"><a class="btn btn-green btn-sm" href="derman-{p['slug']}.html">Tərkib və təlimat</a>
<a class="btn btn-outline btn-sm" href="tel:{PHONE_RAW}">Sifariş</a></div></div></article>"""


def write(name, html):
    (ROOT / name).write_text(html, encoding="utf-8")
    print("wrote", name)


# --------------------------------------------------------------------------- pages
def jsonld():
    return f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Pharmacy","name":"Kardio Aptek","telephone":"{PHONE_RAW}","address":{{"@type":"PostalAddress","streetAddress":"S. Mirzəyev küçəsi (Qara Qarayev metrostansiyası yaxınlığı)","addressLocality":"Bakı","postalCode":"AZ1002","addressCountry":"AZ"}},"openingHours":"Mo-Su 09:00-22:00","foundingDate":"{YEAR}"}}</script>"""


def home():
    feat = "".join(product_card(p) for p in PRODUCTS)
    imgs = "".join(f'<img src="assets/img/{p["card"]}" alt="{p["name"]}" loading="lazy">' for p in PRODUCTS)
    services = [
        ("pill", "Məhsul seçimi", "Ürək-damar sağlamlığı, vitaminlər, immunitet və oynaq üçün məhsullar."),
        ("chat", "Əczaçı məsləhəti", "Tərkib, doza və saxlanma qaydaları barədə aydın izahat."),
        ("phone", "Telefonla sifariş", f"{PHONE_SHOW} nömrəsinə zəng edərək məhsulu əvvəlcədən ayırdın."),
        ("shield", "Təhlükəsizlik", "Son istifadə tarixi və seriya nömrəsi yoxlanılmış məhsullar."),
    ]
    sv = "".join(f'<div class="card reveal"><div class="icon">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in services)
    body = head(SITE, "Kardio Aptek — ürək-damar sağlamlığı, vitaminlər və gündəlik rifah üçün məhsullar, əczaçı məsləhəti. Zəng: " + PHONE_SHOW, jsonld()) + header("index.html") + f"""
<section class="hero"><div class="container">
<div><span class="eyebrow">Kardio Aptek · {YEAR}-ci ildən</span>
<h1>Ürəyiniz üçün <span>etibarlı</span> ünvan</h1>
<p class="lead">Keyfiyyətli məhsullar, peşəkar əczaçı məsləhəti və səmimi xidmət — sağlamlığınız üçün hər zaman yanınızdayıq.</p>
<div class="actions"><a class="btn btn-primary" href="dermanlar.html">Məhsullara bax</a><a class="btn btn-outline" href="tel:{PHONE_RAW}">📞 {PHONE_SHOW}</a></div>
<div class="hero-badges"><span>Tərkibi açıq göstərilir</span><span>Peşəkar məsləhət</span><span>{HOURS}</span></div></div>
<div class="hero-visual"><div class="stack">{imgs}</div><div class="pulse">{ICON['ecg']} Sağlam ürək — sağlam həyat</div></div>
</div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">Məhsullarımız</span><h2>Seçilmiş məhsullar</h2>
<p class="lead">Hər məhsulun tərkibi, istifadə qaydası və qablaşdırma şəkilləri ayrıca səhifədə təqdim olunur.</p></div>
<div class="grid g4">{feat}</div>
<p class="center" style="margin-top:28px"><a class="btn btn-green" href="dermanlar.html">Bütün məhsullar →</a></p>
</div></section>

<section class="section alt"><div class="container">
<div class="section-head center"><span class="eyebrow">Xidmətlər</span><h2>Niyə Kardio Aptek?</h2></div>
<div class="grid g4">{sv}</div></div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">Necə işləyir</span><h2>Sifariş üç addımda</h2></div>
<div class="steps">
<div class="step reveal"><h3>Zəng edin</h3><p>{PHONE_SHOW} nömrəsinə zəng edin və ya WhatsApp-da yazın.</p></div>
<div class="step reveal"><h3>Məsləhət alın</h3><p>Əczaçı tərkib və istifadə qaydası barədə məlumat verəcək.</p></div>
<div class="step reveal"><h3>Məhsulu götürün</h3><p>Seçdiyiniz məhsulu aptekimizdən əldə edin.</p></div>
</div></div></section>

<section class="section alt"><div class="container"><div class="notice green reveal"><strong>Vacib məlumat.</strong> Saytdakı BAQM (bioloji aktiv qida məhsulu) kateqoriyalı məhsullar dərman vasitəsi deyil, xəstəliklərin müalicəsi məqsədilə istifadə edilməməlidir və normal qidalanmanı əvəz etmir. Hamiləlik, laktasiya, xəstəlik və ya dərman qəbulu zamanı mütləq həkimlə məsləhətləşin.</div></div></section>
{cta_block()}""" + footer()
    write("index.html", body)


def about():
    vals = [("heart", "Qayğı", "Hər müştəriyə fərdi yanaşır, sualları səbirlə cavablandırırıq."),
            ("shield", "Etibar", "Tərkibi açıq göstərilən, tarixi və seriyası yoxlanılmış məhsullar təklif edirik."),
            ("book", "Məlumatlandırma", "Düzgün və anlaşıqlı məlumat — sağlam seçimin əsasıdır.")]
    v = "".join(f'<div class="card reveal"><div class="icon red">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in vals)
    body = head("Haqqımızda", "Kardio Aptek haqqında: missiyamız, dəyərlərimiz və xidmət prinsiplərimiz.") + header("haqqimizda.html") + page_hero(
        "Haqqımızda", "Kardio Aptek — ürək sağlamlığına və gündəlik rifaha diqqət yetirən müasir apteklərdən biri.", ["Haqqımızda"]) + f"""
<section class="section"><div class="container grid g2" style="align-items:center;gap:44px">
<div class="reveal"><span class="eyebrow">Biz kimik</span><h2>Ürək sağlamlığına diqqət edən müasir aptek</h2>
<p>Kardio Aptek {YEAR}-cü ildə Bakıda, Qara Qarayev metrostansiyasının yaxınlığında fəaliyyətə başlayıb. Məqsədimiz hər müştəriyə rahat, etibarlı və anlaşıqlı xidmət göstərməkdir.</p>
<p>Təklif etdiyimiz hər məhsul üçün tərkib, doza, istehsalçı və son istifadə tarixi açıq şəkildə göstərilir. Saytdakı məhsul səhifələrində qablaşdırma şəkilləri və tərkib cədvəli də yerləşdirilib ki, qərarı məlumatlı şəkildə verəsiniz.</p>
<a class="btn btn-green" href="dermanlar.html">Məhsullarımıza baxın</a></div>
<div class="reveal"><div class="card" style="padding:12px;background:var(--green-soft)"><div class="grid g2" style="gap:10px">
{"".join(f'<img src="assets/img/{p["card"]}" alt="{p["name"]}" style="background:#fff;border-radius:12px;aspect-ratio:1;object-fit:contain;padding:6px" loading="lazy">' for p in PRODUCTS)}
</div></div></div></div></section>

<section class="section alt"><div class="container"><div class="section-head center"><span class="eyebrow">Dəyərlərimiz</span><h2>Nəyə əsaslanırıq</h2></div>
<div class="grid g3">{v}</div></div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">Missiya və baxış</span><h2>Hara getdiyimizi bilirik</h2></div>
<div class="mv">
<div class="mv-card mission reveal"><span class="mv-ico">{ICON['heart']}</span><h3>Missiyamız</h3>
<p>Hər kəsin sağlamlıq barədə düzgün məlumata və keyfiyyətli məhsullara rahat çıxışını təmin etmək; müştərini məlumatlı seçim etməyə yönəltmək.</p></div>
<div class="mv-card vision reveal"><span class="mv-ico">{ICON['ecg']}</span><h3>Baxışımız</h3>
<p>Ürək-damar sağlamlığı və gündəlik rifah sahəsində Bakıda ən çox güvənilən apteklərdən birinə çevrilmək.</p></div></div>

<div class="pillars">
<div class="pillar reveal"><b>01</b><h3>Şəffaflıq</h3><p>Tərkib, istehsalçı, seriya və tarixlər gizlədilmir — hamısı məhsul səhifəsindədir.</p></div>
<div class="pillar reveal"><b>02</b><h3>Məsuliyyət</h3><p>BAQM və dərman vasitəsi fərqini aydın bildiririk, həkim məsləhətini əvəz etdiyimizi iddia etmirik.</p></div>
<div class="pillar reveal"><b>03</b><h3>Əlçatanlıq</h3><p>Zəng, WhatsApp və ya birbaşa aptekə gələrək suallarınıza cavab ala bilərsiniz.</p></div>
<div class="pillar reveal"><b>04</b><h3>Davamlı inkişaf</h3><p>Məhsul çeşidini və xidməti müştəri rəyləri əsasında yaxşılaşdırırıq.</p></div>
</div>

<div class="promise reveal"><div><h3>Bizim sözümüz</h3><p>Hər müştəriyə eyni hörmət, hər sualına dürüst cavab.</p></div>
<ul><li>Son istifadə tarixi keçmiş məhsul satmırıq</li><li>Məhsulu uyğun şəraitdə saxlayırıq</li><li>Dozanı aşmamaq barədə xəbərdarlıq edirik</li><li>Ciddi hallarda həkimə yönləndiririk</li></ul></div>
</div></section>
{cta_block()}""" + footer()
    write("haqqimizda.html", body)


def catalog():
    chips = "".join(f'<button class="chip{" active" if k == "all" else ""}" data-filter="{k}" type="button">{t}</button>' for k, t in CATS)
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = head("Dərmanlar", "Kardio Aptek məhsulları: Karno Mer, Depomer D3+K2, Revimer, Chondramer — tərkib, doza və qablaşdırma şəkilləri.") + header("dermanlar.html") + page_hero(
        "Dərmanlar və sağlamlıq məhsulları", "Hər məhsulun tərkibi, istifadə qaydası və qablaşdırma şəkilləri ilə tanış olun.", ["Dərmanlar"]) + f"""
<section class="section"><div class="container">
<div class="notice reveal" style="margin-bottom:28px"><strong>Diqqət:</strong> Aşağıdakı məhsullar BAQM (bioloji aktiv qida məhsulu) və ya tibbi vasitədir — <strong>dərman vasitəsi deyil</strong>. Xəstəliklərin müalicəsi məqsədilə istifadə edilməməlidir. İstifadədən əvvəl həkimlə məsləhətləşin.</div>
<div class="toolbar"><div class="chips" role="group" aria-label="Kateqoriya">{chips}</div>
<input id="q" class="search" type="search" placeholder="Məhsul axtar…" aria-label="Məhsul axtar"></div>
<div class="grid g4">{cards}</div>
<p class="empty">Axtarışa uyğun məhsul tapılmadı. Zəng edin: <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></p>
</div></section>{cta_block()}""" + footer()
    write("dermanlar.html", body)


def li(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def detail(p):
    rows = "".join(
        f"<tr><td>{e(a)}<small>{e(b)}</small></td><td>{e(c)}</td></tr>" for a, b, c in p["ing"])
    gal = "".join(
        f'<button class="shot" type="button" data-full="assets/img/{f}" data-cap="{e(c)}"><img src="assets/img/{f}" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></button>'
        for f, c in p["gallery"])
    ids = []
    if p["reg"]:
        ids.append(f"Qeydiyyat №: {p['reg']}")
    if p["extra"]:
        ids.append(p["extra"])
    ids_html = f'<li>{e(" · ".join(ids))}</li>' if ids else ""
    others = "".join(product_card(o) for o in PRODUCTS if o["slug"] != p["slug"])
    body = head(p["name"], f"{p['name']} — {p['short']} Tərkib, doza və əks göstərişlər.") + header("dermanlar.html") + page_hero(
        p["name"], p["short"], ['<a href="dermanlar.html">Dərmanlar</a>', p["name"]]) + f"""
<section class="section"><div class="container">
<div class="detail">
<div class="reveal"><div class="main-img"><img src="assets/img/{p['head']}" alt="{p['name']} qutusu"></div>
<p style="margin-top:14px"><a class="btn btn-primary" href="tel:{PHONE_RAW}">📞 Sifariş: {PHONE_SHOW}</a></p></div>
<div class="reveal">
<span class="tag {p['kindcls']}">{p['kind']}</span>
<h2 style="margin-top:10px">{p['name']}</h2>
<p class="lead" style="font-size:1rem">{p['indication']}</p>
<div class="facts">
<div class="fact"><small>Buraxılış forması</small><b>{p['form']}</b></div>
<div class="fact"><small>Qablaşdırma</small><b>{p['pack']}</b></div>
<div class="fact"><small>Aptekdən buraxılma</small><b>{p['rx']}</b></div>
<div class="fact"><small>Yararlılıq müddəti</small><b>{p['shelf'].split('.')[0]}</b></div></div>

<div class="info-block"><h3>Tərkibi</h3>
<table class="ing"><thead><tr><th>Maddə</th><th style="text-align:right">Miqdar</th></tr></thead>
<caption style="caption-side:top;padding-bottom:8px">{p['comp_title']}</caption><tbody>{rows}</tbody></table></div>
<div class="info-block"><h3>Köməkçi maddələr</h3><p>{p['excip']}</p></div>
<div class="info-block"><h3>İstifadə qaydası və doza</h3>{li(p['dose'])}</div>
<div class="info-block"><h3>Əks göstərişlər</h3>{li(p['contra'])}</div>
<div class="info-block"><h3>Saxlanma şəraiti</h3><p>{p['storage']}</p></div>
<div class="info-block"><h3>İstehsalçı və məlumatlar</h3><ul>
<li><b>İstehsalçı:</b> {e(p['mfr'])}</li><li><b>Ticarət nişanı:</b> {e(p['brand'])}</li>
<li><b>Seriya:</b> {p['series']} · <b>İstehsal:</b> {p['made']} · <b>Son istifadə:</b> {p['exp']}</li>{ids_html}</ul></div>

<div class="notice" style="margin-top:26px"><strong>{"Tibbi vasitədir, dərman vasitəsi deyil." if p['kind']!='BAQM' else "Dərman vasitəsi deyil. Bioloji aktiv qida məhsuludur."}</strong>
Tövsiyə edilən sutkalıq dozanı keçməyin. Uşaqların əli çatmayan yerdə saxlayın. Hamiləlik və laktasiya dövründə, xəstəlik və ya dərman istifadəsi zamanı həkimlə məsləhətləşin.</div>
</div></div></div></section>

<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">Qablaşdırma</span><h2>{p['name']} — qablaşdırma şəkilləri</h2>
<p class="lead">Şəkli böyütmək üçün üzərinə klikləyin.</p></div><div class="gallery">{gal}</div></div></section>

<section class="section"><div class="container"><div class="section-head"><h2>Digər məhsullar</h2></div><div class="grid g3">{others}</div></div></section>""" + footer()
    write(f"derman-{p['slug']}.html", body)


def services():
    items = [
        ("pill", "Məhsul satışı", "Ürək-damar sağlamlığı, vitamin, immunitet və oynaq üçün məhsullar."),
        ("chat", "Əczaçı məsləhəti", "Məhsulun tərkibi, dozası, saxlanması və əks göstərişləri barədə məlumat."),
        ("phone", "Telefonla sifariş", f"{PHONE_SHOW} nömrəsinə zəng və ya WhatsApp vasitəsilə məhsulun mövcudluğunu öyrənin."),
        ("clock", "Tarixlərin yoxlanması", "Təqdim olunan məhsulların seriya və son istifadə tarixi diqqətlə yoxlanılır."),
        ("ecg", "Ürək sağlamlığı məlumatı", "Həyat tərzi və qidalanma üzrə ümumi məlumat materialları."),
        ("drop", "Düzgün saxlama tövsiyələri", "Məhsulların temperatur və rütubət şərtlərinə uyğun saxlanması barədə təlimat."),
    ]
    cards = "".join(f'<div class="card reveal"><div class="icon">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)
    body = head("Xidmətlər", "Kardio Aptek xidmətləri: məhsul satışı, əczaçı məsləhəti, telefonla sifariş.") + header("xidmetler.html") + page_hero(
        "Xidmətlərimiz", "Sizə rahat və etibarlı xidmət göstərmək üçün buradayıq.", ["Xidmətlər"]) + f"""
<section class="section"><div class="container"><div class="grid g3">{cards}</div></div></section>
<section class="section alt"><div class="container"><div class="notice green reveal"><strong>Qeyd:</strong> Əczaçı məsləhəti məlumat xarakterlidir və həkimin diaqnoz və müalicəsini əvəz etmir. Ciddi şikayətlər zamanı həkimə müraciət edin.</div></div></section>
{cta_block()}""" + footer()
    write("xidmetler.html", body)


def tips():
    tips = [
        ("Duz və doymuş yağları azaldın", "Gündəlik duz qəbulunu məhdudlaşdırmaq qan təzyiqinə nəzarət üçün vacibdir. Tərəvəz, meyvə, bütövdənli məhsullar və balıq daha yaxşı seçimdir."),
        ("Hərəkət edin", "Həftədə ən azı 150 dəqiqə orta intensivlikli fiziki fəaliyyət (sürətli yeriş, üzgüçülük) ürək-damar sağlamlığına dəstək olur."),
        ("Siqaretdən imtina edin", "Siqaret ürək-damar xəstəlikləri üçün əsas risk amillərindən biridir. İmtina etmək üçün həkimdən kömək ala bilərsiniz."),
        ("Təzyiqi və çəkini izləyin", "Qan təzyiqini müntəzəm ölçün, normal bədən çəkisini qoruyun və həkim yoxlamalarını buraxmayın."),
        ("Keyfiyyətli yuxu və stress idarəsi", "Gündə 7–8 saat yuxu və stressi azaldan vərdişlər (gəzinti, nəfəs məşqləri) ümumi sağlamlığa müsbət təsir edir."),
        ("Vitamin və əlavələri düşünərək seçin", "Vitamin və BAQM-lar tarazlı qidalanmanı əvəz etmir. D vitamini kimi məhsulları qəbul etməzdən əvvəl dozanı həkimlə razılaşdırın."),
    ]
    t = "".join(f'<div class="card tip reveal"><div class="num">{i+1}</div><div><h3>{a}</h3><p>{b}</p></div></div>' for i, (a, b) in enumerate(tips))
    body = head("Sağlamlıq məsləhətləri", "Ürək sağlamlığı üçün ümumi məsləhətlər: qidalanma, hərəkət, təzyiqə nəzarət və vitaminlərə düzgün yanaşma.") + header("meslehetler.html") + page_hero(
        "Sağlamlıq məsləhətləri", "Ürək sağlamlığı və gündəlik rifah üçün sadə, ümumi tövsiyələr.", ["Məsləhətlər"]) + f"""
<section class="section"><div class="container"><div class="grid g2">{t}</div>
<div class="notice reveal" style="margin-top:28px"><strong>Xəbərdarlıq:</strong> Bu səhifədəki məlumatlar ümumi xarakter daşıyır və fərdi tibbi məsləhəti əvəz etmir. Sinə ağrısı, nəfəs darlığı, huşun itməsi kimi hallarda dərhal təcili yardım çağırın.</div></div></section>
{cta_block()}""" + footer()
    write("meslehetler.html", body)


def faq():
    qa = [
        ("BAQM nədir?", "BAQM — bioloji aktiv qida məhsulu deməkdir. Bu məhsullar dərman vasitəsi deyil; qidaya əlavə kimi nəzərdə tutulub və xəstəliklərin müalicəsi üçün istifadə edilməməlidir."),
        ("Məhsulları reseptsiz almaq olarmı?", "Saytda təqdim olunan məhsulların hamısı aptekdən reseptsiz buraxılır. Yenə də istifadədən əvvəl həkim və ya əczaçı ilə məsləhətləşməyiniz tövsiyə olunur."),
        ("Hamiləlik və ya əmizdirmə dövründə istifadə edə bilərəmmi?", "Məhsulların etiketində göstərildiyi kimi, hamiləlik və laktasiya dövründə, həmçinin xəstəlik və ya dərman qəbulu zamanı mütləq həkimlə məsləhətləşin."),
        ("Uşaqlar üçün uyğundurmu?", "Depomer D3+K2 etiketdə 2–4 və 4–14 yaş qrupları üçün uyğun göstərilib. Digər məhsullar üçün həkim məsləhəti lazımdır. Bütün məhsulları uşaqların əli çatmayan yerdə saxlayın."),
        ("Məhsulları necə saxlamalıyam?", "Etiketlərə əsasən 25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə saxlayın."),
        ("Yararlılıq müddəti nə qədərdir?", "Təqdim etdiyimiz məhsulların yararlılıq müddəti istehsal tarixindən 3 ildir. Tarix qutunun üzərində göstərilir; müddət bitdikdən sonra istifadə etməyin."),
        ("Məhsulu necə sifariş edə bilərəm?", f"{PHONE_SHOW} nömrəsinə zəng edin, WhatsApp-da yazın və ya Əlaqə səhifəsindəki formadan istifadə edin."),
        ("Dozanı artırsam daha tez təsir edərmi?", "Xeyr. Tövsiyə edilən sutkalıq dozanı keçməyin. Dozanın dəyişdirilməsi yalnız həkim məsləhəti ilə mümkündür."),
    ]
    d = "".join(f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>" for q, a in qa)
    body = head("Tez-tez verilən suallar", "Kardio Aptek: BAQM, doza, saxlanma, yararlılıq müddəti və sifariş barədə tez-tez verilən suallar.") + header("suallar.html") + page_hero(
        "Tez-tez verilən suallar", "Ən çox soruşulan suallara qısa cavablar.", ["Suallar"]) + f"""
<section class="section"><div class="container" style="max-width:820px">{d}</div></section>{cta_block()}""" + footer()
    write("suallar.html", body)


def contact():
    body = head("Əlaqə", f"Kardio Aptek ilə əlaqə: {PHONE_SHOW}. WhatsApp və ya zəng ilə sifariş və məsləhət.") + header("elaqe.html") + page_hero(
        "Əlaqə", "Sualınız və ya sifarişiniz üçün bizimlə əlaqə saxlayın.", ["Əlaqə"]) + f"""
<section class="section"><div class="container contact-grid">
<div class="reveal"><ul class="contact-list">
<li><div class="icon red">{ICON['phone']}</div><div><small>Telefon</small><b><a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></b></div></li>
<li><div class="icon">{ICON['wa']}</div><div><small>WhatsApp</small><b><a href="https://wa.me/{WA}" target="_blank" rel="noopener">Mesaj yazın</a></b></div></li>
<li><div class="icon">{ICON['pin']}</div><div><small>Ünvan</small><b>{CITY}</b></div></li>
<li><div class="icon">{ICON['clock']}</div><div><small>İş saatları</small><b>{HOURS}</b></div></li></ul></div>
<div class="card reveal"><h3>Bizə yazın</h3><p style="margin-bottom:16px">Formu doldurduqda mesajınız WhatsApp-da hazır şəkildə açılacaq.</p>
<form id="contact-form" data-wa="{WA}">
<label for="n">Adınız</label><input class="input" id="n" name="name" required autocomplete="name">
<label for="p">Telefon</label><input class="input" id="p" name="phone" type="tel" required autocomplete="tel">
<label for="t">Mövzu</label><select class="input" id="t" name="topic"><option>Məhsul haqqında sual</option><option>Sifariş</option><option>Digər</option></select>
<label for="m">Mesaj</label><textarea class="input" id="m" name="message" required></textarea>
<button class="btn btn-primary" type="submit">WhatsApp-da göndər</button></form></div>
</div></section>
<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">Xəritə</span><h2>Bizi necə tapmaq olar</h2>
<p class="lead">Qara Qarayev metrostansiyasının yaxınlığında, S. Mirzəyev küçəsində yerləşirik.</p></div>
<div class="map reveal"><iframe title="Kardio Aptek — Google Maps" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<p style="margin-top:18px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="{MAP_DIR}" target="_blank" rel="noopener">📍 Yol tarifi al</a><a class="btn btn-outline" href="{MAP_LINK}" target="_blank" rel="noopener">Google Maps-də aç</a></p></div></section>""" + footer()
    write("elaqe.html", body)


def privacy():
    body = head("Məxfilik siyasəti", "Kardio Aptek saytının məxfilik siyasəti.") + header("") + page_hero(
        "Məxfilik siyasəti", f"Son yenilənmə: {YEAR}", ["Məxfilik"]) + f"""
<section class="section"><div class="container prose">
<h2>Toplanan məlumatlar</h2><p>Bu sayt serverdə şəxsi məlumat saxlamır. Əlaqə formasında daxil etdiyiniz məlumatlar (ad, telefon, mesaj) yalnız sizin təsdiqinizlə WhatsApp vasitəsilə bizə göndərilir.</p>
<h2>Üçüncü tərəflər</h2><p>Sayt şrift yükləmək üçün Google Fonts xidmətindən istifadə edir; bu zaman brauzeriniz həmin xidmətə sorğu göndərir.</p>
<h2>Tibbi məlumat</h2><p>Saytdakı məlumatlar məlumat xarakterlidir, həkim məsləhətini və diaqnozu əvəz etmir.</p>
<h2>Əlaqə</h2><p>Suallarınız üçün: <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a>.</p></div></section>""" + footer()
    write("mexfiyyet.html", body)


def not_found():
    body = head("Səhifə tapılmadı", "Axtardığınız səhifə mövcud deyil.") + header("") + f"""
<section class="section"><div class="container center"><span class="eyebrow">404</span><h1>Səhifə tapılmadı</h1>
<p class="lead">Axtardığınız səhifə köçürülüb və ya mövcud deyil.</p><p><a class="btn btn-green" href="index.html">Ana səhifəyə qayıt</a></p></div></section>""" + footer()
    write("404.html", body)


def static():
    (ROOT / "favicon.svg").write_text(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1), encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")


if __name__ == "__main__":
    home(); about(); catalog()
    for p in PRODUCTS:
        detail(p)
    services(); tips(); faq(); contact(); privacy(); not_found(); static()
