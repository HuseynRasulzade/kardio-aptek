#!/usr/bin/env python3
"""Static site generator for Kardio Aptek. Run: python3 build.py  -> writes *.html next to this file."""
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "Kardio Aptek"
PHONE_RAW = "+994502779434"
PHONE_SHOW = "+994 50 277 94 34"
WA = PHONE_RAW.lstrip("+")
YEAR = 2024
MAPQ = "Qara Qarayev metrostansiyası, S. Mirzəyev küçəsi, Bakı, Azerbaijan"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=" + MAPQ.replace(" ", "+")
MAP_DIR = "https://www.google.com/maps/dir/?api=1&destination=" + MAPQ.replace(" ", "+")

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


# =========================================================================== i18n
LANGS = ["az", "en", "ru"]
LANG = "az"
LANG_NAMES = {"az": "AZ", "en": "EN", "ru": "RU"}
HTML_LANG = {"az": "az", "en": "en", "ru": "ru"}
OG_LOCALE = {"az": "az_AZ", "en": "en_US", "ru": "ru_RU"}


def T(a, en, ru):
    return {"az": a, "en": en, "ru": ru}[LANG]


def pfx():
    return "" if LANG == "az" else "../"


def outdir():
    d = ROOT if LANG == "az" else ROOT / LANG
    d.mkdir(exist_ok=True)
    return d


def units(x):
    """Convert Azerbaijani unit abbreviations in an amount string."""
    x = re.sub(r"(?<=\d) q$", " " + T("q", "g", "г"), x)
    return (x.replace("mkq", T("mkq", "mcg", "мкг")).replace("mq", T("mq", "mg", "мг"))
             .replace("BV", T("BV", "IU", "МЕ")).replace("50 000", T("50 000", "50,000", "50 000")))


def hours():
    return T("Hər gün 09:00 – 22:00", "Every day 09:00 – 22:00", "Ежедневно 09:00 – 22:00")


def city():
    return T("Qara Qarayev metrostansiyası yaxınlığı, S. Mirzəyev küçəsi, Bakı, AZ1002, Azərbaycan",
             "Near Qara Qarayev metro station, S. Mirzayev street, Baku, AZ1002, Azerbaijan",
             "Рядом со станцией метро «Гара Гараев», ул. С. Мирзоева, Баку, AZ1002, Азербайджан")


def map_embed():
    return "https://maps.google.com/maps?q=" + MAPQ.replace(" ", "+") + "&z=16&output=embed&hl=" + LANG


NAV = [
    ("index.html", ("Ana səhifə", "Home", "Главная")),
    ("haqqimizda.html", ("Haqqımızda", "About us", "О нас")),
    ("dermanlar.html", ("Dərmanlar", "Medicines", "Препараты")),
    ("xidmetler.html", ("Xidmətlər", "Services", "Услуги")),
    ("meslehetler.html", ("Məsləhətlər", "Health tips", "Советы")),
    ("suallar.html", ("Suallar", "FAQ", "Вопросы")),
    ("elaqe.html", ("Əlaqə", "Contact", "Контакты")),
]


def nav_label(t):
    return T(*t)


# --------------------------------------------------------------------------- products
def products_base():
    return [
        dict(
            slug="karno-mer", name="Karno Mer", cat="urek",
            kind=T("BAQM", "Dietary supplement", "БАД"), medical=False,
            short=T("Ürək-damar sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
                    "Recommended to support the function of the cardiovascular system.",
                    "Средство для улучшения функции сердечно-сосудистой системы."),
            form=T("Kapsul", "Capsule", "Капсулы"),
            pack=T("30 kapsul (2×15 blister), karton qutu", "30 capsules (2×15 blister), cardboard box", "30 капсул (2×15 блистер), картонная коробка"),
            card="karno-card.jpg", head="karno-qutu.jpg",
            comp_title=T("1 kapsulun tərkibi", "Composition per capsule", "Состав на 1 капсулу"),
            ing=[(("L-karnitin", "L-carnitine", "L-карнитин"), "L-carnitine", "500 mq"),
                 (("Koenzim Q10", "Coenzyme Q10", "Коэнзим Q10"), "Coenzyme Q10", "40 mq"),
                 (("Kuersetin", "Quercetin", "Кверцетин"), "Quercetin", "25 mq")],
            excip=T("Mikrokristallik sellüloza, maqnezium stearat, jelatin, oliqofruktoza, nişasta.",
                    "Microcrystalline cellulose, magnesium stearate, gelatin, oligofructose, starch.",
                    "Микрокристаллическая целлюлоза, стеарат магния, желатин, олигофруктоза, крахмал."),
            indication=T("Ürək-damar sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
                         "Recommended to improve the function of the cardiovascular system.",
                         "Рекомендуется для улучшения функции сердечно-сосудистой системы."),
            dose=T(["Böyüklər: 1 kapsul gündə 1 dəfə daxilə qəbul edilir.", "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər."],
                   ["Adults: 1 capsule once a day, taken orally.", "Dose and age limits may only be changed on a doctor's advice."],
                   ["Взрослым: по 1 капсуле 1 раз в день внутрь.", "Дозировку и возрастные ограничения можно изменять только по рекомендации врача."]),
            contra=T(["Məhsulun tərkibindəki hər hansı komponentə qarşı fərdi həssaslıq."],
                     ["Individual sensitivity to any component of the product."],
                     ["Индивидуальная чувствительность к любому из компонентов продукта."]),
            storage=T("25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə.",
                      "At a temperature not above 25 °C, in a dry place protected from light and out of reach of children.",
                      "При температуре не выше 25 °C, в сухом, защищённом от света и недоступном для детей месте."),
            shelf=T("3 il", "3 years", "3 года"),
            mfr=T("FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", "FITO LAB MMC (Azerbaijan, Absheron district, Saray settlement, AZ0121)",
                  "FITO LAB MMC (Азербайджан, Абшеронский р-н, пос. Сарай, AZ0121)"),
            brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
            series="FTL/1246", made="10.2024", exp="10.2027", reg="01-Q-00589", extra="QOST/ГОСТ 23058-89",
            gallery=[("karno-qutu.jpg", T("Karno Mer — qutunun ön üzü", "Karno Mer — front of the box", "Karno Mer — лицевая сторона коробки")),
                     ("karno-terkib.jpg", T("Tərkib və istifadə qaydası", "Composition and directions", "Состав и способ применения")),
                     ("karno-vereq.jpg", T("İstifadə təlimatı vərəqi", "Instruction leaflet", "Инструкция по применению")),
                     ("karno-istehsalci.jpg", T("İstehsalçı və sertifikatlar", "Manufacturer and certificates", "Производитель и сертификаты")),
                     ("karno-tarix.jpg", T("Seriya, istehsal və son istifadə tarixi", "Batch, production and expiry date", "Серия, дата производства и срок годности"))],
        ),
        dict(
            slug="depomer-d3-k2", name="Depomer D3+K2", cat="vitamin",
            kind=T("BAQM", "Dietary supplement", "БАД"), medical=False,
            short=T("D3 və K2 vitaminlərinin əlavə mənbəyi — 15 ml damcı məhlul (50 000 BV).",
                    "An additional source of vitamins D3 and K2 — 15 ml oral drops (50,000 IU).",
                    "Дополнительный источник витаминов D3 и K2 — капли для приёма внутрь 15 мл (50 000 МЕ)."),
            form=T("Daxilə qəbul üçün məhlul-damcı", "Oral solution (drops)", "Раствор-капли для приёма внутрь"),
            pack=T("15 ml şüşə flakon, karton qutu (1 ml = 25 damcı)", "15 ml glass vial, cardboard box (1 ml = 25 drops)", "Стеклянный флакон 15 мл, картонная коробка (1 мл = 25 капель)"),
            card="depomer-card.jpg", head="depomer-qutu.jpg",
            comp_title=T("15 ml-in tərkibi (1 ml = 25 damcı)", "Composition per 15 ml (1 ml = 25 drops)", "Состав на 15 мл (1 мл = 25 капель)"),
            ing=[(("Vitamin D3", "Vitamin D3", "Витамин D3"), "Cholecalciferol", "50 000 BV"),
                 (("Vitamin K2", "Vitamin K2", "Витамин K2"), "Menaquinone", "200 mkq")],
            excip=T("Zeytun yağı.", "Olive oil.", "Оливковое масло."),
            indication=T("D3 və K2 vitaminlərinin əlavə mənbəyi kimi tövsiyə olunan vasitə.",
                         "Recommended as an additional source of vitamins D3 and K2.",
                         "Рекомендуется как дополнительный источник витаминов D3 и K2."),
            dose=T(["2–4 yaş arası uşaqlar: 1 damcı gündə 1 dəfə.", "4–14 yaş arası uşaqlar: 2 damcı gündə 1 dəfə.",
                    "14 yaşdan yuxarı uşaqlar və böyüklər: 4 damcı gündə 1 dəfə.",
                    "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər.", "İstifadədən əvvəl flakonu çalxalayın."],
                   ["Children 2–4 years: 1 drop once a day.", "Children 4–14 years: 2 drops once a day.",
                    "Children over 14 and adults: 4 drops once a day.",
                    "Dose and age limits may only be changed on a doctor's advice.", "Shake the vial before use."],
                   ["Дети 2–4 лет: 1 капля 1 раз в день.", "Дети 4–14 лет: 2 капли 1 раз в день.",
                    "Дети старше 14 лет и взрослые: 4 капли 1 раз в день.",
                    "Дозировку и возрастные ограничения можно изменять только по рекомендации врача.", "Перед применением флакон взболтать."]),
            contra=T(["Tərkibindəki hər hansı inqrediyentə qarşı fərdi həssaslıq.", "D hipervitaminozu, hiperkalsiemiya, hiperkalsiuriya.",
                      "Böyrək çatmazlığı, böyrək daşları xəstəliyi.", "Ağciyər vərəminin aktiv forması."],
                     ["Individual sensitivity to any ingredient.", "Hypervitaminosis D, hypercalcemia, hypercalciuria.",
                      "Renal failure, kidney stone disease.", "Active form of pulmonary tuberculosis."],
                     ["Индивидуальная чувствительность к любому из компонентов.", "Гипервитаминоз D, гиперкальциемия, гиперкальциурия.",
                      "Почечная недостаточность, мочекаменная болезнь.", "Активная форма туберкулёза лёгких."]),
            storage=T("25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə.",
                      "At a temperature not above 25 °C, in a dry place protected from light and out of reach of children.",
                      "При температуре не выше 25 °C, в сухом, защищённом от света и недоступном для детей месте."),
            shelf=T("3 il", "3 years", "3 года"),
            mfr=T("FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", "FITO LAB MMC (Azerbaijan, Absheron district, Saray settlement, AZ0121)",
                  "FITO LAB MMC (Азербайджан, Абшеронский р-н, пос. Сарай, AZ0121)"),
            brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
            series="DK1012", made="02.2026", exp="02.2029", reg="01-Q-00589",
            extra=T("AQTA qeydiyyat № MQ-05-001738 · TŞ AZ 1006595881.003-2022", "AFSA reg. no. MQ-05-001738 · TC AZ 1006595881.003-2022", "Рег. № АПБА MQ-05-001738 · ТУ AZ 1006595881.003-2022"),
            gallery=[("depomer-qutu.jpg", T("Depomer D3+K2 — qutunun ön üzü", "Depomer D3+K2 — front of the box", "Depomer D3+K2 — лицевая сторона коробки")),
                     ("depomer-terkib.jpg", T("Tərkib və doza (Azərbaycan dilində)", "Composition and dosage (Azerbaijani)", "Состав и дозировка (на азербайджанском)")),
                     ("depomer-terkib-en.jpg", T("Composition and dosage (English)", "Composition and dosage (English)", "Состав и дозировка (на английском)")),
                     ("depomer-vereq.jpg", T("İstifadə təlimatı vərəqi", "Instruction leaflet", "Инструкция по применению"))],
        ),
        dict(
            slug="revimer", name="Revimer", cat="immun",
            kind=T("BAQM", "Dietary supplement", "БАД"), medical=False,
            short=T("İmmun sistemin fəaliyyətini yaxşılaşdırmaq məqsədilə — 10 flakon × 15 ml məhlul.",
                    "To support the immune system — 10 vials × 15 ml solution.",
                    "Для поддержки иммунной системы — 10 флаконов × 15 мл раствора."),
            form=T("Daxilə qəbul üçün məhlul", "Oral solution", "Раствор для приёма внутрь"),
            pack=T("15 ml şüşə flakon, No.10, karton qutu", "15 ml glass vial, No.10, cardboard box", "Стеклянный флакон 15 мл, №10, картонная коробка"),
            card="revimer-card.jpg", head="revimer-qutu.jpg",
            comp_title=T("15 ml-in tərkibi", "Composition per 15 ml", "Состав на 15 мл"),
            ing=[(("Arı südü tozu, liofilizə olunmuş", "Royal jelly, lyophilized powder", "Маточное молочко, лиофилизированный порошок"), "Royal jelly lyophilized powder", "200 mq"),
                 (("Barbados albalısı meyvə ekstraktı tozu", "Barbados cherry fruit extract powder", "Экстракт плодов барбадосской вишни (порошок)"), "Malpighia emarginata", "150 mq"),
                 (("Qaragilə meyvə konsentratı", "Bilberry fruit concentrate", "Концентрат плодов черники"), "Vaccinium myrtillus", "750 mq"),
                 (("Qara kəndələş meyvə konsentratı", "Black elderberry fruit concentrate", "Концентрат плодов чёрной бузины"), "Sambucus nigra", "500 mq"),
                 (("Böyürtkən meyvə ekstraktı", "Blackberry fruit extract", "Экстракт плодов ежевики"), "Rubus fruticosus", "375 mq")],
            excip=T("Deionizə olunmuş su, ksantan qətranı, limon turşusu, moruq aroması, kalium sorbat, natrium benzoat, sukraloza.",
                    "Deionized water, xanthan gum, citric acid, raspberry flavour, potassium sorbate, sodium benzoate, sucralose.",
                    "Деионизированная вода, ксантановая камедь, лимонная кислота, ароматизатор малины, сорбат калия, бензоат натрия, сукралоза."),
            indication=T("İmmun sistemin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.",
                         "Recommended to support the function of the immune system.",
                         "Рекомендуется для улучшения функции иммунной системы."),
            dose=T(["Böyüklər: 15 ml gündə 1 dəfə.", "Digər hallarda həkim məsləhəti ilə tövsiyə oluna bilər.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                   ["Adults: 15 ml once a day.", "In other cases, may be recommended on a doctor's advice.", "Do not exceed the recommended daily dose."],
                   ["Взрослым: 15 мл 1 раз в день.", "В остальных случаях — по рекомендации врача.", "Не превышайте рекомендуемую суточную дозу."]),
            contra=T(["Məhsulun tərkibindəki hər hansı komponentə qarşı həssaslıq."],
                     ["Sensitivity to any component of the product."],
                     ["Повышенная чувствительность к любому из компонентов продукта."]),
            storage=T("25 °C-dən yüksək olmayan temperaturda, quru və uşaqların əli çatmayan yerdə.",
                      "At a temperature not above 25 °C, in a dry place out of reach of children.",
                      "При температуре не выше 25 °C, в сухом, недоступном для детей месте."),
            shelf=T("3 il", "3 years", "3 года"),
            mfr=T("EVA MED MMC (Azərbaycan Respublikası, Bakı)", "EVA MED MMC (Republic of Azerbaijan, Baku)", "EVA MED MMC (Азербайджанская Республика, Баку)"),
            brand="EVA MED Medicine",
            series="116", made="05.01.2026", exp="05.01.2029", reg="", extra="",
            gallery=[("revimer-qutu.jpg", T("Revimer — qutunun ön üzü", "Revimer — front of the box", "Revimer — лицевая сторона коробки")),
                     ("revimer-terkib.jpg", T("Tərkib, köməkçi maddələr və doza", "Composition, excipients and dosage", "Состав, вспомогательные вещества и дозировка")),
                     ("revimer-vereq.jpg", T("İstifadə təlimatı vərəqi (1)", "Instruction leaflet (1)", "Инструкция по применению (1)")),
                     ("revimer-vereq2.jpg", T("İstifadə təlimatı vərəqi (2)", "Instruction leaflet (2)", "Инструкция по применению (2)")),
                     ("revimer-istehsalci.jpg", T("İstehsalçı və saxlanma şəraiti", "Manufacturer and storage conditions", "Производитель и условия хранения")),
                     ("revimer-tarix.jpg", T("İstehsal və son istifadə tarixi", "Production and expiry date", "Дата производства и срок годности"))],
        ),
        dict(
            slug="chondramer", name="Chondramer", cat="oynaq",
            kind=T("Tibbi vasitə", "Medical device", "Медицинское изделие"), medical=True,
            short=T("Oynaq və əzələ ağrıları üçün istifadə olunan gel — 75 q.", "A gel for joint and muscle pain — 75 g.", "Гель при болях в суставах и мышцах — 75 г."),
            form=T("Yerli istifadə üçün gel", "Gel for topical use", "Гель для наружного применения"),
            pack=T("75 q plastik tubik, karton qutu", "75 g plastic tube, cardboard box", "Пластиковая туба 75 г, картонная коробка"),
            card="chondramer-card.jpg", head="chondramer-qutu.jpg",
            comp_title=T("75 q gel-in tərkibi", "Composition per 75 g of gel", "Состав на 75 г геля"),
            ing=[(("Glukozamin sulfat", "Glucosamine sulphate", "Глюкозамина сульфат"), "Glucosamine sulphate", "800 mq"),
                 (("Xondroitin sulfat", "Chondroitin sulphate", "Хондроитина сульфат"), "Chondroitin sulphate", "200 mq"),
                 (("Metilsulfonilmetan", "Methylsulphonylmethane", "Метилсульфонилметан"), "Methylsulphonylmethane", "200 mq"),
                 (("Bosvelliya ekstraktı", "Boswellia serrata extract", "Экстракт босвеллии пильчатой"), "Boswellia serrata extract", "120 mq"),
                 (("Evkalipt yağı", "Eucalyptus oil", "Масло эвкалипта"), "Eucalyptus oil", "50 mq"),
                 (("Kəklikotu yağı", "Thyme oil", "Масло тимьяна"), "Thyme oil", "10 mq"),
                 (("Mixək yağı", "Clove oil", "Масло гвоздики"), "Clove oil", "5 mq"),
                 (("Rozmarin yağı", "Rosemary oil", "Масло розмарина"), "Rosemary oil", "12 mq"),
                 (("Kamfora", "Camphor", "Камфора"), "Camphor", "20 mq"),
                 (("Mentol", "Menthol", "Ментол"), "Menthol", "150 mq")],
            excip=T("Aromaterapiya yağları (zəncəfil, lavanda, zirə, qoz, portağal yağı), qliserin, karbomer.",
                    "Aromatherapy oils (ginger, lavender, cumin, walnut, orange), glycerine, carbomer.",
                    "Ароматерапевтические масла (имбирь, лаванда, зира, грецкий орех, апельсин), глицерин, карбомер."),
            indication=T("Oynaq və əzələ ağrıları üçün istifadə olunan tibbi vasitə.", "A medical device used for joint and muscle pain.", "Медицинское изделие, применяемое при болях в суставах и мышцах."),
            dose=T(["Yerli və xaricdən tətbiq edin. Birbaşa oynaqların və əzələlərin nahiyəsinə masaj edərək sürtün.",
                    "İstənilən effekti əldə etmək üçün təmizlənmiş dəri nahiyəsinə gündə ən azı 2–3 dəfə yerli olaraq istifadə edilməlidir.",
                    "Doza və yaş həddi yalnız həkim məsləhəti ilə dəyişdirilə bilər."],
                   ["For topical external use. Apply directly to the joint and muscle area and rub in with a massage.",
                    "For the desired effect, apply to cleansed skin at least 2–3 times a day.",
                    "Dose and age limits may only be changed on a doctor's advice."],
                   ["Для местного наружного применения. Наносить непосредственно на область суставов и мышц, втирая массажными движениями.",
                    "Для достижения желаемого эффекта наносить на очищенную кожу не менее 2–3 раз в день.",
                    "Дозировку и возрастные ограничения можно изменять только по рекомендации врача."]),
            contra=T(["Tərkibində olan hər hansı komponentə qarşı fərdi həssaslıq."],
                     ["Individual sensitivity to any component."],
                     ["Индивидуальная чувствительность к любому из компонентов."]),
            storage=T("25 °C-dən yüksək olmayan temperaturda, quru, işıq düşməyən və uşaqların əli çatmayan yerdə.",
                      "At a temperature not above 25 °C, in a dry place away from light and out of reach of children.",
                      "При температуре не выше 25 °C, в сухом, защищённом от света и недоступном для детей месте."),
            shelf=T("3 il", "3 years", "3 года"),
            mfr=T("FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", "FITO LAB MMC (Azerbaijan, Absheron district, Saray settlement, AZ0121)",
                  "FITO LAB MMC (Азербайджан, Абшеронский р-н, пос. Сарай, AZ0121)"),
            brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki",
            series="CM1011", made="02.2025", exp="02.2028", reg="", extra="",
            gallery=[("chondramer-qutu.jpg", T("Chondramer — qutunun ön üzü", "Chondramer — front of the box", "Chondramer — лицевая сторона коробки")),
                     ("chondramer-terkib.jpg", T("Tərkib və istifadə qaydası", "Composition and directions", "Состав и способ применения")),
                     ("chondramer-vereq.jpg", T("İstifadə təlimatı vərəqi", "Instruction leaflet", "Инструкция по применению")),
                     ("chondramer-istehsalci.jpg", T("İstehsalçı, seriya və tarixlər", "Manufacturer, batch and dates", "Производитель, серия и даты"))],
        ),
    ]




# --------------------------------------------------------------------------- additional products (added 13 Oct)
STORE_LO = lambda: T("25 °C-dən aşağı temperaturda, quru, sərin, günəş şüası düşməyən və uşaqların əli çatmayan yerdə.",
                     "At a temperature below 25 °C, in a dry, cool place away from sunlight and out of reach of children.",
                     "При температуре ниже 25 °C, в сухом, прохладном месте, защищённом от солнечных лучей и недоступном для детей.")
STORE_HI = lambda: T("25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə.",
                     "At a temperature not above 25 °C, in a dry place protected from light and out of reach of children.",
                     "При температуре не выше 25 °C, в сухом, защищённом от света и недоступном для детей месте.")
EVA = lambda: T("EVA MED MMC (Azərbaycan Respublikası, Bakı)", "EVA MED MMC (Republic of Azerbaijan, Baku)", "EVA MED MMC (Азербайджанская Республика, Баку)")
SH3 = lambda: T("3 il", "3 years", "3 года")
BAQM = lambda: T("BAQM", "Dietary supplement", "БАД")
TIBBI = lambda: T("Tibbi vasitə", "Medical device", "Медицинское изделие")
CAUTION_SENS = lambda: T(["Məhsulun tərkibindəki hər hansı komponentə qarşı həssaslıq."],
                         ["Sensitivity to any component of the product."],
                         ["Повышенная чувствительность к любому из компонентов продукта."])
MAXDOSE = lambda: T("Tövsiyə edilən sutkalıq dozanı keçməyin.", "Do not exceed the recommended daily dose.", "Не превышайте рекомендуемую суточную дозу.")


def cap(az, en, ru):
    return T(az, en, ru)


def products_new():
    box = lambda n: cap("qutunun ön üzü", "front of the box", "лицевая сторона коробки")
    leaf = lambda n="": cap("İstifadə təlimatı vərəqi", "Instruction leaflet", "Инструкция по применению") + n
    side = lambda: cap("Qutunun yan üzü", "Side of the box", "Боковая сторона коробки")
    comp = lambda: cap("Tərkib və istifadə qaydası", "Composition and directions", "Состав и способ применения")
    aa = [("Alanin", "Alanine", "Аланин", "1"), ("Asparagin", "Asparagine", "Аспарагин", "1"), ("Aspartik turşusu", "Aspartic acid", "Аспарагиновая кислота", "1"),
          ("Sistein", "Cysteine", "Цистеин", "1"), ("Qlutamik turşusu", "Glutamic acid", "Глутаминовая кислота", "1"), ("Qlutamin", "Glutamine", "Глутамин", "1"),
          ("Qlisin", "Glycine", "Глицин", "2"), ("Serin", "Serine", "Серин", "1"), ("Tirozin", "Tyrosine", "Тирозин", "1"), ("Prolin", "Proline", "Пролин", "1"),
          ("Arginin", "Arginine", "Аргинин", "1.2"), ("Histidin", "Histidine", "Гистидин", "0.7"), ("İzoleysin", "Isoleucine", "Изолейцин", "1.18"),
          ("Leysin", "Leucine", "Лейцин", "3.66"), ("Lizin HCl", "Lysine HCl", "Лизина гидрохлорид", "5"), ("Metionin", "Methionine", "Метионин", "1.84"),
          ("Fenilalanin", "Phenylalanine", "Фенилаланин", "1"), ("Treonin", "Threonine", "Треонин", "0.85"), ("Triptofan", "Tryptophan", "Триптофан", "1"),
          ("Valin", "Valine", "Валин", "1.34")]
    meta_ing = [(("L-" + a, "L-" + b, "L-" + c), "", d + " mq") for a, b, c, d in aa] + [(("Vitamin C", "Vitamin C", "Витамин C"), "", "100 mq")]
    return [
        dict(slug="aktimer", name="Aktimer", cat="urek", kind=BAQM(), medical=False,
             short=T("Ürək, beyin və enerji mübadiləsini dəstəkləyən məhlul — 150 ml.", "A solution supporting the heart, brain and energy metabolism — 150 ml.", "Раствор для поддержки сердца, мозга и энергетического обмена — 150 мл."),
             form=T("Daxilə qəbul üçün məhlul", "Oral solution", "Раствор для приёма внутрь"),
             pack=T("150 ml şüşə flakon, karton qutu", "150 ml glass vial, cardboard box", "Стеклянный флакон 150 мл, картонная коробка"),
             card="aktimer-card.jpg", head="aktimer-qutu.jpg",
             comp_title=T("10 ml-in tərkibi", "Composition per 10 ml", "Состав на 10 мл"),
             ing=[(("L-Karnitin", "L-Carnitine", "L-Карнитин"), "L-carnitine", "300 mq"), (("Koenzim Q10", "Coenzyme Q10", "Коэнзим Q10"), "Coenzyme Q10", "10 mq"),
                  (("Vitamin B12", "Vitamin B12", "Витамин B12"), "Cyanocobalamin", "5 mkq"), (("Xolin bitartrat", "Choline bitartrate", "Холина битартрат"), "Choline bitartrate", "10 mq")],
             excip=T("Sukraloza, portağal dadlandırıcısı, ksantan qətranı, natrium benzoat, kalium sorbat, limon turşusu, deionlaşdırılmış su.",
                     "Sucralose, orange flavouring, xanthan gum, sodium benzoate, potassium sorbate, citric acid, deionized water.",
                     "Сукралоза, ароматизатор апельсина, ксантановая камедь, бензоат натрия, сорбат калия, лимонная кислота, деионизированная вода."),
             indication=T("Ürək, beyin və enerji mübadiləsini eyni anda dəstəkləyən, fiziki və əqli gərginliyi aradan qaldırmaq məqsədi ilə tövsiyə olunan vasitə.",
                          "Recommended to support the heart, brain and energy metabolism at the same time and to help relieve physical and mental strain.",
                          "Рекомендуется для одновременной поддержки сердца, мозга и энергетического обмена, а также для снятия физического и умственного напряжения."),
             dose=T(["4–14 yaş: 5 ml gündə 1 dəfə.", "14 yaşdan yuxarı və böyüklər: 10 ml gündə 1 dəfə.", "Qida qəbulundan sonra daxilə qəbul olunur.", "4 yaşdan aşağı uşaqlar üçün istifadə olunmur.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                    ["Ages 4–14: 5 ml once a day.", "Over 14 and adults: 10 ml once a day.", "Take orally after meals.", "Not for children under 4 years.", "Do not exceed the recommended daily dose."],
                    ["4–14 лет: 5 мл 1 раз в день.", "Старше 14 лет и взрослые: 10 мл 1 раз в день.", "Принимать внутрь после еды.", "Не применять детям младше 4 лет.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_LO(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="114", made="01.2026", exp="01.2029", reg="", extra="",
             gallery=[("aktimer-qutu.jpg", "Aktimer — " + box(0)), ("aktimer-terkib.jpg", comp()), ("aktimer-yan.jpg", side()),
                      ("aktimer-vereq.jpg", leaf(" (1)")), ("aktimer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="laktomer-max", name="Laktomer-Max", cat="immun", kind=BAQM(), medical=False,
             short=T("İmmun sistemin fəaliyyətini yaxşılaşdırmaq üçün bitki ekstraktları — 100 ml.", "Plant extracts to support the immune system — 100 ml.", "Растительные экстракты для поддержки иммунной системы — 100 мл."),
             form=T("Daxilə qəbul üçün məhlul", "Oral solution", "Раствор для приёма внутрь"),
             pack=T("100 ml şüşə flakon, karton qutu", "100 ml glass vial, cardboard box", "Стеклянный флакон 100 мл, картонная коробка"),
             card="laktomer-card.jpg", head="laktomer-qutu.jpg",
             comp_title=T("2 ml-in tərkibi", "Composition per 2 ml", "Состав на 2 мл"),
             ing=[(("Qara qoz qabığının ekstraktı", "Black walnut hull extract", "Экстракт кожуры чёрного ореха"), "Black Walnut Hull Extract", "500 mq"),
                  (("Şirin kök (Glycyrrhiza glabra) ekstraktı", "Licorice root (Glycyrrhiza glabra) extract", "Экстракт корня солодки (Glycyrrhiza glabra)"), "Licorice Root Extract", "400 mq"),
                  (("Balqabaq toxumunun ekstraktı", "Pumpkin seed extract", "Экстракт семян тыквы"), "Pumpkin Seed Extract", "250 mq"),
                  (("Dağtərəxunu ekstraktı", "Yarrow extract", "Экстракт тысячелистника"), "Yarrow Extract", "250 mq"),
                  (("Qərənfil çiçəyinin yağı", "Clove flower oil", "Масло цветков гвоздики"), "Clove Flower Oil", "250 mq"),
                  (("Sarımsaq ekstraktı", "Garlic extract", "Экстракт чеснока"), "Garlic Extract", "250 mq")],
             excip=T("Təmizlənmiş su, sorbitol, sukraloza, limon turşusu, kalium sorbat, natrium benzoat, təbii aroma.",
                     "Purified water, sorbitol, sucralose, citric acid, potassium sorbate, sodium benzoate, natural flavour.",
                     "Очищенная вода, сорбитол, сукралоза, лимонная кислота, сорбат калия, бензоат натрия, натуральный ароматизатор."),
             indication=T("İmmun sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.", "Recommended to support the function of the immune system.", "Рекомендуется для улучшения функции иммунной системы."),
             dose=T(["2–3 yaş: 2.5 ml gündə 1 dəfə.", "4–12 yaş: 5 ml gündə 1 dəfə.", "12 yaş və böyüklər: 10 ml gündə 1 dəfə.", "Kurs müddəti: 7–14 gün.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                    ["Ages 2–3: 2.5 ml once a day.", "Ages 4–12: 5 ml once a day.", "Age 12 and over, adults: 10 ml once a day.", "Course: 7–14 days.", "Do not exceed the recommended daily dose."],
                    ["2–3 года: 2,5 мл 1 раз в день.", "4–12 лет: 5 мл 1 раз в день.", "Старше 12 лет и взрослые: 10 мл 1 раз в день.", "Курс: 7–14 дней.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_LO(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="", made="", exp="", reg="", extra="",
             gallery=[("laktomer-qutu.jpg", "Laktomer-Max — " + box(0)), ("laktomer-terkib.jpg", comp()), ("laktomer-doza.jpg", T("Doza və saxlanma", "Dosage and storage", "Дозировка и хранение")),
                      ("laktomer-vereq.jpg", leaf(" (1)")), ("laktomer-vereq2.jpg", leaf(" (2)")), ("laktomer-vereq3.jpg", leaf(" (3)"))]),
        dict(slug="fargimer", name="Fargimer", cat="tenefus", kind=TIBBI(), medical=True,
             short=T("Kombinə olunmuş boğaz spreyi — 30 ml.", "A combined throat spray — 30 ml.", "Комбинированный спрей для горла — 30 мл."),
             form=T("Daxilə qəbul üçün məhlul-sprey", "Oral solution (spray)", "Раствор-спрей для приёма внутрь"),
             pack=T("30 ml şüşə flakon, karton qutu", "30 ml glass vial, cardboard box", "Стеклянный флакон 30 мл, картонная коробка"),
             card="fargimer-card.jpg", head="fargimer-qutu.jpg",
             comp_title=T("30 ml-in tərkibi", "Composition per 30 ml", "Состав на 30 мл"),
             ing=[(("Sürvə yarpaqlarının maye ekstraktı", "Sage leaf liquid extract", "Жидкий экстракт листьев шалфея"), "Salviae officinalis folia", "0.01 q"),
                  (("Müalicəvi gülümbahar gülünün maye ekstraktı", "Calendula flower liquid extract", "Жидкий экстракт цветков календулы"), "Calendulae officinalis flores", "0.01 q"),
                  (("İtburnu güllərinin və toxumlarının yağı", "Rosehip flower and seed oil", "Масло цветков и семян шиповника"), "Oleum rosae pinuae", "0.03 q"),
                  (("Ayıpəncəsi kökünün cövhəri", "Burdock root tincture", "Настойка корня лопуха"), "Arctium lappa L. Ext. et tincture", "0.01 q"),
                  (("Metilen abısının suda məhlulu", "Methylene blue aqueous solution", "Водный раствор метиленового синего"), "Methylenum coeruleum", "1 %")],
             excip=T("Propilen qlikol, kalium sorbat, kalium yodid, distillə edilmiş su.", "Propylene glycol, potassium sorbate, potassium iodide, distilled water.", "Пропиленгликоль, сорбат калия, йодид калия, дистиллированная вода."),
             indication=T("Ağız boşluğu və boğaz xəstəliklərinin profilaktika və müalicəsində istifadəsi tövsiyə olunan köməkçi tibbi vasitə.",
                          "A supporting medical device recommended for the prevention and treatment of oral cavity and throat conditions.",
                          "Вспомогательное медицинское изделие для профилактики и лечения заболеваний полости рта и горла."),
             about=T("Fargimer kombinə olunmuş boğaz spreyidir.", "Fargimer is a combined throat spray.", "Fargimer — комбинированный спрей для горла."),
             uses=T(["Yuxarı tənəffüs yollarının infeksion iltihabı xəstəliklərində köməkçi vasitə kimi: tonzilit, farinqit, larinqit, afoniya, disfoniya", "Orofaringeal infeksiyalar",
                     "Səpkili və xoralı stomatitlər", "Yenidoğulmuşun ağız boşluğunda süd yarası (kandidoz)", "Gingivit, parodontoz", "Boğazda ağrı və qaşınma hissi",
                     "Ağız boşluğunda xoşagəlməz qoxu", "Cərrahi əməliyyatdan sonra"],
                    ["As an aid in infectious inflammatory diseases of the upper respiratory tract: tonsillitis, pharyngitis, laryngitis, aphonia, dysphonia", "Oropharyngeal infections",
                     "Rash and ulcerative stomatitis", "Oral thrush (candidiasis) in newborns", "Gingivitis, periodontosis", "Sore and itchy throat",
                     "Unpleasant breath", "After surgery"],
                    ["Как вспомогательное средство при инфекционно-воспалительных заболеваниях верхних дыхательных путей: тонзиллит, фарингит, ларингит, афония, дисфония", "Орофарингеальные инфекции",
                     "Сыпные и язвенные стоматиты", "Молочница (кандидоз) полости рта у новорождённых", "Гингивит, пародонтоз", "Боль и зуд в горле",
                     "Неприятный запах изо рта", "После хирургических операций"]),
             dose=T(["Daxilə qəbul olunur (qəbul vaxtı üçün qablaşdırmadakı yazıya baxın).", "0–6 ay: 1 dozadan gündə 1–2 dəfə.", "6–12 ay: 1–2 dozadan gündə 1–2 dəfə.",
                     "1–3 yaş: 2 dozadan gündə 3 dəfə.", "3–6 yaş: 2 dozadan gündə 3–4 dəfə.", "6 yaş və böyüklər: 1–2 dozadan gündə 5–6 dəfə, yəni hər 3–4 saatdan bir püskürtmək məsləhətdir.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                    ["Taken orally (see the packaging photos for the timing relative to meals).", "0–6 months: 1 dose 1–2 times a day.", "6–12 months: 1–2 doses 1–2 times a day.",
                     "1–3 years: 2 doses 3 times a day.", "3–6 years: 2 doses 3–4 times a day.", "6 years and older: 1–2 doses 5–6 times a day, i.e. every 3–4 hours.", "Do not exceed the recommended daily dose."],
                    ["Принимается внутрь (время приёма относительно еды см. на фото упаковки).", "0–6 месяцев: 1 доза 1–2 раза в день.", "6–12 месяцев: 1–2 дозы 1–2 раза в день.",
                     "1–3 года: 2 дозы 3 раза в день.", "3–6 лет: 2 дозы 3–4 раза в день.", "С 6 лет и взрослые: 1–2 дозы 5–6 раз в день, то есть каждые 3–4 часа.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=T(["Etiketdə əks göstəriş qeyd olunmayıb — istifadədən əvvəl həkimlə məsləhətləşin."], ["No contraindications are listed on the label — consult a doctor before use."], ["На этикетке противопоказания не указаны — перед применением проконсультируйтесь с врачом."]),
             storage=T("18–25 °C temperaturda, birbaşa istilik və günəş şüası düşməyən, uşaqların əli çatmayan yerdə.", "At 18–25 °C, away from direct heat and sunlight and out of reach of children.", "При температуре 18–25 °C, вдали от прямого тепла и солнечных лучей, в недоступном для детей месте."),
             shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine", series="098", made="21.11.2025", exp="21.11.2028", reg="", extra="",
             gallery=[("fargimer-qutu.jpg", "Fargimer — " + box(0)), ("fargimer-terkib.jpg", comp()), ("fargimer-gostericiler.jpg", T("İstifadə sahəsi, saxlanma və tarixlər", "Uses, storage and dates", "Применение, хранение и даты")),
                      ("fargimer-vereq.jpg", leaf(" (1)")), ("fargimer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="maqnimer", name="Maqnimer", cat="vitamin", kind=BAQM(), medical=False,
             short=T("Maqnezium və B vitaminlərinin əlavə mənbəyi — 30 kapsul.", "An additional source of magnesium and B vitamins — 30 capsules.", "Дополнительный источник магния и витаминов группы B — 30 капсул."),
             form=T("Kapsul", "Capsule", "Капсулы"),
             pack=T("3×10 (№30) blister, karton qutu", "3×10 (No. 30) blister, cardboard box", "3×10 (№30) блистер, картонная коробка"),
             card="maqnimer-card.jpg", head="maqnimer-qutu.jpg",
             comp_title=T("1 kapsulun tərkibi", "Composition per capsule", "Состав на 1 капсулу"),
             ing=[(("Maqnezium laktat (Maqnezium 56,5 mq)", "Magnesium lactate (Magnesium 56.5 mg)", "Лактат магния (магний 56,5 мг)"), "Magnesium Lactate", "470 mq"),
                  (("Vitamin B1 (Tiamin)", "Vitamin B1 (Thiamine)", "Витамин B1 (тиамин)"), "Thiamine", "5 mq"),
                  (("Vitamin B6 (Piridoksin hidroxlorid)", "Vitamin B6 (Pyridoxine hydrochloride)", "Витамин B6 (пиридоксина гидрохлорид)"), "Pyridoxine hydrochloride", "5 mq")],
             excip=T("Maltodekstrin, maqnezium stearat, silikon dioksid, jelatin.", "Maltodextrin, magnesium stearate, silicon dioxide, gelatin.", "Мальтодекстрин, стеарат магния, диоксид кремния, желатин."),
             indication=T("Maqnezium və B vitaminin əlavə mənbəyi kimi tövsiyə olunan vasitə.", "Recommended as an additional source of magnesium and B vitamins.", "Рекомендуется как дополнительный источник магния и витаминов группы B."),
             dose=T(["Böyüklər: 1 kapsul gündə 1 dəfə.", "Digər hallarda həkim məsləhəti ilə qəbul edilməlidir.", "Tövsiyə olunan sutkalıq dozanı keçməyin."],
                    ["Adults: 1 capsule once a day.", "In other cases, only on a doctor's advice.", "Do not exceed the recommended daily dose."],
                    ["Взрослым: 1 капсула 1 раз в день.", "В остальных случаях — только по рекомендации врача.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_LO(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="106", made="01.11.2025", exp="01.11.2028", reg="", extra="",
             gallery=[("maqnimer-qutu.jpg", "Maqnimer — " + box(0)), ("maqnimer-terkib.jpg", comp()), ("maqnimer-tarix.jpg", T("Doza, seriya və tarixlər", "Dosage, batch and dates", "Дозировка, серия и даты")),
                      ("maqnimer-yan.jpg", side()), ("maqnimer-vereq.jpg", leaf(" (1)")), ("maqnimer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="metabomer", name="Metabomer", cat="vitamin", kind=BAQM(), medical=False,
             short=T("Amin turşuları və C vitamini kompleksi — 50 ml damcı.", "An amino-acid and vitamin C complex — 50 ml drops.", "Комплекс аминокислот и витамина C — капли 50 мл."),
             form=T("Daxilə qəbul üçün məhlul-damcı", "Oral solution (drops)", "Раствор-капли для приёма внутрь"),
             pack=T("50 ml şüşə flakon, karton qutu", "50 ml glass vial, cardboard box", "Стеклянный флакон 50 мл, картонная коробка"),
             card="metabomer-card.jpg", head="metabomer-qutu.jpg",
             comp_title=T("2 ml-in tərkibi", "Composition per 2 ml", "Состав на 2 мл"),
             ing=meta_ing,
             excip=T("Deionizə su, qliserol, sukraloza, moruq ətri, natrium benzoat, kalium sorbat, sitrik turşusu.", "Deionized water, glycerol, sucralose, raspberry flavour, sodium benzoate, potassium sorbate, citric acid.", "Деионизированная вода, глицерин, сукралоза, аромат малины, бензоат натрия, сорбат калия, лимонная кислота."),
             indication=T("Amin turşularının və C vitamininin əlavə mənbəyi kimi tövsiyə olunan vasitə.", "Recommended as an additional source of amino acids and vitamin C.", "Рекомендуется как дополнительный источник аминокислот и витамина C."),
             dose=T(["4 yaşdan yuxarı uşaqlar: 2 ml (40 damcı) gündə 1 dəfə.", "Tövsiyə edilən sutkalıq dozanı keçməyin."], ["Children over 4 years: 2 ml (40 drops) once a day.", "Do not exceed the recommended daily dose."], ["Дети старше 4 лет: 2 мл (40 капель) 1 раз в день.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_HI(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="", made="", exp="", reg="", extra="",
             gallery=[("metabomer-qutu.jpg", "Metabomer — " + box(0)), ("metabomer-terkib.jpg", comp()), ("metabomer-yan.jpg", side()),
                      ("metabomer-vereq.jpg", leaf(" (1)")), ("metabomer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="vipomer-uro", name="Vipomer-Uro", cat="sidik", kind=BAQM(), medical=False,
             short=T("Sidik-ifrazat sisteminin fəaliyyətini yaxşılaşdırmaq üçün — 30 kapsul.", "To support the function of the urinary system — 30 capsules.", "Для улучшения функции мочевыделительной системы — 30 капсул."),
             form=T("Kapsul", "Capsule", "Капсулы"),
             pack=T("N30 kapsul (2×15) blister, içlik vərəqəsi ilə karton qutuda", "30 capsules (2×15) blister, in a cardboard box with a leaflet", "30 капсул (2×15) блистер, в картонной коробке с вкладышем"),
             card="vipomer-card.jpg", head="vipomer-qutu.jpg",
             comp_title=T("1 kapsulun tərkibi", "Composition per capsule", "Состав на 1 капсулу"),
             ing=[(("Adi mərcanı meyvəsinin ekstraktı", "Cranberry fruit extract", "Экстракт плодов клюквы"), "Vaccinium oxycoccos fruit extract", "250 mq"),
                  (("D-mannoza", "D-mannose", "D-манноза"), "D-mannose", "200 mq"), (("Kalium sitrat", "Potassium citrate", "Цитрат калия"), "Potassium citrate", "10 mq"),
                  (("Maqnezium sitrat", "Magnesium citrate", "Цитрат магния"), "Magnesium citrate", "10 mq"), (("Natrium sitrat", "Sodium citrate", "Цитрат натрия"), "Sodium citrate", "30 mq")],
             excip=T("Jelatin, qarğıdalı nişastası.", "Gelatin, corn starch.", "Желатин, кукурузный крахмал."),
             indication=T("Sidik-ifrazat sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.", "Recommended to support the function of the urinary system.", "Рекомендуется для улучшения функции мочевыделительной системы."),
             dose=T(["Böyüklər: 1 kapsul gündə 1 dəfə.", "Tövsiyə edilən sutkalıq dozanı keçməyin."], ["Adults: 1 capsule once a day.", "Do not exceed the recommended daily dose."], ["Взрослым: 1 капсула 1 раз в день.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=T(["Məhsulun tərkibindəki hər hansı komponentə qarşı fərdi həssaslıq."], ["Individual sensitivity to any component of the product."], ["Индивидуальная чувствительность к любому из компонентов продукта."]),
             storage=STORE_HI(), shelf=SH3(),
             mfr=T("FITO LAB MMC (Azərbaycan, Abşeron r-nu, Saray qəs., AZ0121)", "FITO LAB MMC (Azerbaijan, Absheron district, Saray settlement, AZ0121)", "FITO LAB MMC (Азербайджан, Абшеронский р-н, пос. Сарай, AZ0121)"),
             brand="POLSHA PHARMA SP.Z.O.O., Jana Pawla str/II 3bf/1 05-091 Zabki", series="UT0412", made="01.2025", exp="01.2028", reg="01-Q-00589", extra="QOST/ГОСТ 23058-89",
             gallery=[("vipomer-qutu.jpg", "Vipomer-Uro — " + box(0)), ("vipomer-terkib.jpg", comp()), ("vipomer-vereq.jpg", leaf()),
                      ("vipomer-istehsalci.jpg", T("İstehsalçı və sertifikatlar", "Manufacturer and certificates", "Производитель и сертификаты")), ("vipomer-tarix.jpg", T("Seriya, istehsal və son istifadə tarixi", "Batch, production and expiry date", "Серия, дата производства и срок годности"))]),
        dict(slug="venomer", name="Venomer", cat="vitamin", kind=BAQM(), medical=False,
             short=T("Dəmirin əlavə mənbəyi — fol turşusu, C və B12 ilə, 100 ml sirop.", "An additional source of iron with folic acid, vitamin C and B12 — 100 ml.", "Дополнительный источник железа с фолиевой кислотой, витамином C и B12 — 100 мл."),
             form=T("Daxilə qəbul üçün məhlul", "Oral solution", "Раствор для приёма внутрь"),
             pack=T("100 ml şüşə flakon, karton qutu", "100 ml glass vial, cardboard box", "Стеклянный флакон 100 мл, картонная коробка"),
             card="venomer-card.jpg", head="venomer-qutu.jpg",
             comp_title=T("5 ml-in tərkibi", "Composition per 5 ml", "Состав на 5 мл"),
             ing=[(("Dəmir fumarat (Dəmir – 11,2 mq)", "Ferrous fumarate (iron – 11.2 mg)", "Фумарат железа (железо – 11,2 мг)"), "Ferrous fumarate", "35 mq"),
                  (("Fol turşusu", "Folic acid", "Фолиевая кислота"), "Folic acid", "350 mkq"), (("Vitamin C", "Vitamin C", "Витамин C"), "Vitamin C", "80 mq"), (("Vitamin B12", "Vitamin B12", "Витамин B12"), "Vitamin B12", "3 mkq")],
             excip=T("Kalium sorbat, natrium benzoat, deionlaşdırılmış su.", "Potassium sorbate, sodium benzoate, deionized water.", "Сорбат калия, бензоат натрия, деионизированная вода."),
             indication=T("Dəmirin əlavə mənbəyi kimi tövsiyə olunan vasitə.", "Recommended as an additional source of iron.", "Рекомендуется как дополнительный источник железа."),
             dose=T(["2–4 yaş: 1.25 ml gündə 1 dəfə.", "4–14 yaş: 2.5 ml gündə 1 dəfə.", "14 yaşdan yuxarı uşaqlar, böyüklər və hamilələr: 5 ml gündə 1 dəfə.", "İstifadədən əvvəl flakonu çalxalayın.", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                    ["Ages 2–4: 1.25 ml once a day.", "Ages 4–14: 2.5 ml once a day.", "Over 14, adults and pregnant women: 5 ml once a day.", "Shake the vial before use.", "Do not exceed the recommended daily dose."],
                    ["2–4 года: 1,25 мл 1 раз в день.", "4–14 лет: 2,5 мл 1 раз в день.", "Старше 14 лет, взрослые и беременные: 5 мл 1 раз в день.", "Перед применением флакон взболтать.", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_HI(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="115", made="11.2025", exp="11.2028", reg="", extra="",
             gallery=[("venomer-qutu.jpg", "Venomer — " + box(0)), ("venomer-terkib.jpg", comp()), ("venomer-yan.jpg", side()),
                      ("venomer-vereq.jpg", leaf(" (1)")), ("venomer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="neframer", name="Neframer", cat="tenefus", kind=TIBBI(), medical=True,
             short=T("Hipertonik dəniz suyu burun spreyi — 50 ml.", "Hypertonic sea-water nasal spray — 50 ml.", "Назальный спрей с гипертонической морской водой — 50 мл."),
             form=T("Daxilə qəbul üçün məhlul-sprey", "Spray solution", "Раствор-спрей"),
             pack=T("50 ml şüşə flakon, karton qutu", "50 ml glass vial, cardboard box", "Стеклянный флакон 50 мл, картонная коробка"),
             card="neframer-card.jpg", head="neframer-qutu.jpg",
             comp_title=T("Tərkibi", "Composition", "Состав"),
             ing=[(("Hipertonik dəniz suyu məhlulu", "Hypertonic sea water solution", "Раствор гипертонической морской воды"), "", "2.2 %")],
             excip=T("Deionizə su, kalium sorbat, natrium benzoat.", "Deionized water, potassium sorbate, sodium benzoate.", "Деионизированная вода, сорбат калия, бензоат натрия."),
             indication=T("Burun boşluğunun gigiyenası üçün nəzərdə tutulub.", "Intended for the hygiene of the nasal cavity.", "Предназначен для гигиены полости носа."),
             about=T("Etiketdə «dərman vasitəsi deyildir, gigiyenik vasitədir» yazılıb; qutunun arxa üzündə isə «tibbi vasitədir» qeyd olunub.",
                     "The label says \"not a medicine, a hygiene product\"; the back of the box also states \"medical device\".",
                     "На этикетке указано «не лекарственное средство, гигиеническое средство»; на обратной стороне коробки — «медицинское изделие»."),
             uses=T(["Burun tıxanıqlığının azaldılması", "Burun selikli qişasının nəmləndirilməsi", "Toz, allergiya, mikrob və digər kirlərin mexaniki təmizlənməsi", "Soyuqdəymə və qrip zamanı burun yollarının gigiyenası", "Ətraf mühitin təsirindən (quru hava, kondisioner, tozlu mühit) qorunma"],
                    ["Reducing nasal congestion", "Moisturising the nasal mucosa", "Mechanical cleansing of dust, allergens, microbes and other impurities", "Nasal hygiene during colds and flu", "Protection from environmental effects (dry air, air conditioning, dusty environments)"],
                    ["Уменьшение заложенности носа", "Увлажнение слизистой оболочки носа", "Механическое очищение от пыли, аллергенов, микробов и других загрязнений", "Гигиена носовых ходов при простуде и гриппе", "Защита от влияния окружающей среды (сухой воздух, кондиционеры, запылённая среда)"]),
             dose=T(["İstifadədən əvvəl flakonu çalxalayın.", "Buruna püskürtmə yolu ilə istifadə olunur.", "Gündə bir neçə dəfə tətbiq oluna bilər.", "İstifadədən əvvəl təlimatı oxuyun."],
                    ["Shake the vial before use.", "Use by spraying into the nose.", "May be applied several times a day.", "Read the instructions before use."],
                    ["Перед применением флакон взболтать.", "Применяется путём распыления в нос.", "Можно применять несколько раз в день.", "Перед применением прочтите инструкцию."]),
             contra=T(["Etiketdə əks göstəriş qeyd olunmayıb — istifadədən əvvəl həkimlə məsləhətləşin."], ["No contraindications are listed on the label — consult a doctor before use."], ["На этикетке противопоказания не указаны — перед применением проконсультируйтесь с врачом."]),
             storage=T("25 °C-dən yüksək olmayan temperaturda, quru, sərin və uşaqların əli çatmayan yerdə.", "At a temperature not above 25 °C, in a dry, cool place out of reach of children.", "При температуре не выше 25 °C, в сухом, прохладном и недоступном для детей месте."),
             shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine", series="105", made="21.11.2025", exp="21.11.2028", reg="", extra="",
             gallery=[("neframer-qutu.jpg", "Neframer — " + box(0)), ("neframer-terkib.jpg", comp()), ("neframer-yan.jpg", side()),
                      ("neframer-vereq.jpg", leaf(" (1)")), ("neframer-vereq2.jpg", leaf(" (2)"))]),
        dict(slug="starbone-calcium", name="StarBone Calcium", cat="oynaq", kind=BAQM(), medical=False,
             short=T("Kalsium, sink, D3 və K1 kompleksi — 60 kapsul.", "A calcium, zinc, D3 and K1 complex — 60 capsules.", "Комплекс кальция, цинка, D3 и K1 — 60 капсул."),
             form=T("Kapsul", "Capsule", "Капсулы"),
             pack=T("№60 (6×10) blister, karton qutu", "No. 60 (6×10) blister, cardboard box", "№60 (6×10) блистер, картонная коробка"),
             card="starbone-card.jpg", head="starbone-qutu.jpg",
             comp_title=T("1 kapsulun tərkibi", "Composition per capsule", "Состав на 1 капсулу"),
             ing=[(("Kalsium karbonat (120 mq elementar kalsium)", "Calcium carbonate (120 mg elemental calcium)", "Карбонат кальция (120 мг элементарного кальция)"), "Calcium carbonate", "300 mq"),
                  (("Sink oksid (4 mq elementar sink)", "Zinc oxide (4 mg elemental zinc)", "Оксид цинка (4 мг элементарного цинка)"), "Zinc oxide", "5 mq"),
                  (("Vitamin D3 (Xolekalsiferol)", "Vitamin D3 (Cholecalciferol)", "Витамин D3 (холекальциферол)"), "Cholecalciferol", "2.5 mkq"),
                  (("Vitamin K1 (Fitomenadion)", "Vitamin K1 (Phytomenadione)", "Витамин K1 (фитоменадион)"), "Phytomenadione", "25 mkq")],
             excip=T("Mikrokristallik sellüloza, maqnezium stearat.", "Microcrystalline cellulose, magnesium stearate.", "Микрокристаллическая целлюлоза, стеарат магния."),
             indication=T("Dayaq-hərəkət sisteminin fəaliyyətini yaxşılaşdırmaq məqsədilə tövsiyə olunan vasitə.", "Recommended to support the function of the musculoskeletal system.", "Рекомендуется для улучшения функции опорно-двигательной системы."),
             dose=T(["12 yaşdan yuxarı uşaqlar və böyüklər: 1 kapsul gündə 1 dəfə (qəbul vaxtı üçün qutudakı yazıya baxın).", "Tövsiyə edilən sutkalıq dozanı keçməyin."],
                    ["Children over 12 and adults: 1 capsule once a day (see the packaging for the timing).", "Do not exceed the recommended daily dose."],
                    ["Дети старше 12 лет и взрослые: 1 капсула 1 раз в день (время приёма см. на упаковке).", "Не превышайте рекомендуемую суточную дозу."]),
             contra=CAUTION_SENS(), storage=STORE_LO(), shelf=SH3(), mfr=EVA(), brand="EVA MED Medicine",
             series="150", made="12.2025", exp="12.2028", reg="", extra="",
             gallery=[("starbone-qutu.jpg", "StarBone Calcium — " + box(0)), ("starbone-terkib.jpg", comp()), ("starbone-yan.jpg", side()), ("starbone-vereq.jpg", leaf())]),
    ]


def products():
    return products_base() + products_new()


def cats():
    return [("all", T("Hamısı", "All", "Все")), ("urek", T("Ürək-damar", "Cardiovascular", "Сердце и сосуды")),
            ("vitamin", T("Vitaminlər və minerallar", "Vitamins & minerals", "Витамины и минералы")), ("immun", T("İmmunitet", "Immunity", "Иммунитет")),
            ("oynaq", T("Sümük, oynaq və əzələ", "Bones, joints & muscles", "Кости, суставы и мышцы")),
            ("tenefus", T("Boğaz və burun", "Throat & nose", "Горло и нос")), ("sidik", T("Sidik sistemi", "Urinary system", "Мочевыделительная система"))]


def rx():
    return T("Reseptsiz", "Over the counter", "Без рецепта")


# --------------------------------------------------------------------------- layout
def lang_switch(page):
    out = []
    for l in LANGS:
        target = ("" if l == "az" else l + "/") + page
        href = ("../" if LANG != "az" else "") + target
        cur = ' aria-current="true"' if l == LANG else ""
        out.append(f'<a href="{href}" hreflang="{l}" lang="{l}"{cur}>{LANG_NAMES[l]}</a>')
    return '<div class="lang" role="group" aria-label="Language">' + "".join(out) + "</div>"


def head(title, desc, page, extra=""):
    home_title = T("Sağlamlığınız üçün etibarlı ünvan", "Your trusted pharmacy for health", "Надёжная аптека для вашего здоровья")
    full = f"{title} | {SITE}" if title != SITE else f"{SITE} — {home_title}"
    P = pfx()
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{("../" if LANG != "az" else "")}{("" if l == "az" else l + "/")}{page}">' for l in LANGS)
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[LANG]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0f766e">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="{OG_LOCALE[LANG]}">
{alts}
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}assets/css/style.css">
{extra}
</head>"""


CUR = ' aria-current="page"'
PHONE_ICON = ICON["phone"].replace("<svg", '<svg width="16" height="16"')


def header(active, page):
    links = "".join(f'<li><a href="{h}"{CUR if h == active else ""}>{nav_label(t)}</a></li>' for h, t in NAV)
    call = T("Zəng et", "Call us", "Позвонить")
    return f"""<body data-close="{T('Bağla', 'Close', 'Закрыть')}" data-prev="{T('Əvvəlki', 'Previous', 'Назад')}" data-next="{T('Növbəti', 'Next', 'Далее')}">
<a class="skip" href="#main">{T('Əsas məzmuna keç', 'Skip to main content', 'Перейти к содержимому')}</a>
<header class="site"><div class="container">
<a class="logo" href="index.html" aria-label="{SITE}">{LOGO}<span>Kardio <b>Aptek</b></span></a>
<nav class="main" id="nav" aria-label="{T('Əsas menyu', 'Main menu', 'Главное меню')}"><ul>{links}</ul></nav>
<div class="header-cta">{lang_switch(page)}<a class="btn btn-primary btn-sm" href="tel:{PHONE_RAW}">{PHONE_ICON} {call}</a>
<button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav" type="button">☰</button></div>
</div></header>
<main id="main">"""


def footer():
    fl = "".join(f'<li><a href="{h}">{nav_label(t)}</a></li>' for h, t in NAV)
    pl = "".join(f'<li><a href="derman-{p["slug"]}.html">{p["name"]}</a></li>' for p in products()[:6])
    P = pfx()
    return f"""</main>
<footer class="site"><div class="container">
<div class="cols">
<div><a class="logo" href="index.html">{LOGO}<span>Kardio Aptek</span></a>
<p style="margin-top:14px">{T('Ürək sağlamlığı və gündəlik rifahınız üçün keyfiyyətli məhsullar, peşəkar məsləhət və səmimi xidmət.',
                              'Quality products, professional advice and friendly service for your heart health and everyday wellbeing.',
                              'Качественные товары, профессиональные консультации и внимательный сервис для здоровья вашего сердца и повседневного благополучия.')}</p></div>
<div><h4>{T('Səhifələr', 'Pages', 'Страницы')}</h4><ul>{fl}</ul></div>
<div><h4>{T('Məhsullar', 'Products', 'Товары')}</h4><ul>{pl}<li><a href="dermanlar.html">{T('Bütün məhsullar →', 'All products →', 'Все товары →')}</a></li></ul></div>
<div><h4>{T('Əlaqə', 'Contact', 'Контакты')}</h4><ul>
<li>📞 <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></li>
<li>💬 <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
<li>🕘 {hours()}</li>
<li>📍 <a href="{MAP_LINK}" target="_blank" rel="noopener">{city()}</a></li>
<li><a href="mexfiyyet.html">{T('Məxfilik siyasəti', 'Privacy policy', 'Политика конфиденциальности')}</a></li></ul></div>
</div>
<div class="legal"><span>© {YEAR} Kardio Aptek. {T('Bütün hüquqlar qorunur.', 'All rights reserved.', 'Все права защищены.')}</span>
<span>{T('Saytdakı məlumatlar məlumat xarakterlidir və həkim məsləhətini əvəz etmir.',
         'The information on this site is for reference only and does not replace medical advice.',
         'Информация на сайте носит справочный характер и не заменяет консультацию врача.')}</span></div>
</div></footer>
<div class="fab"><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON['wa']}</a>
<a class="tel" href="tel:{PHONE_RAW}" aria-label="{T('Zəng et', 'Call us', 'Позвонить')}">{ICON['phone']}</a></div>
<script src="{P}assets/js/main.js" defer></script>
</body></html>"""


def page_hero(title, sub, crumbs=None):
    c = ""
    if crumbs:
        c = f'<div class="crumbs"><a href="index.html">{T("Ana səhifə", "Home", "Главная")}</a> / ' + " / ".join(crumbs) + "</div>"
    return f'<section class="page-hero"><div class="container">{c}<h1>{title}</h1><p>{sub}</p></div></section>'


def cta_block():
    return f"""<section class="section"><div class="container"><div class="cta reveal">
<div><h2>{T('Sualınız var? Bizə zəng edin', 'Have a question? Call us', 'Есть вопрос? Позвоните нам')}</h2><p>{T('Əczaçılarımız məhsullar barədə məlumat verməyə hazırdır.', 'Our pharmacists are happy to tell you more about our products.', 'Наши фармацевты готовы рассказать о продуктах подробнее.')}</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="tel:{PHONE_RAW}">📞 {PHONE_SHOW}</a>
<a class="btn btn-outline" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></div></div></div></section>"""


def product_card(p):
    P = pfx()
    return f"""<article class="card product reveal" data-cat="{p['cat']}">
<a class="thumb" href="derman-{p['slug']}.html" aria-label="{p['name']}"><img src="{P}assets/img/{p['card']}" alt="{p['name']}" loading="lazy"></a>
<div class="body"><span class="tag {'red' if p['medical'] else ''}">{p['kind']}</span><h3>{p['name']}</h3><p class="sub">{p['short']}</p>
<div class="actions"><a class="btn btn-green btn-sm" href="derman-{p['slug']}.html">{T('Tərkib və təlimat', 'Ingredients & leaflet', 'Состав и инструкция')}</a>
<a class="btn btn-outline btn-sm" href="tel:{PHONE_RAW}">{T('Sifariş', 'Order', 'Заказать')}</a></div></div></article>"""


def write(name, html):
    (outdir() / name).write_text(html, encoding="utf-8")
    print("wrote", LANG, name)


def jsonld():
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Pharmacy","name":"Kardio Aptek",'
            f'"telephone":"{PHONE_RAW}","address":{{"@type":"PostalAddress","streetAddress":"S. Mirzəyev küçəsi","addressLocality":"Bakı","postalCode":"AZ1002","addressCountry":"AZ"}},'
            '"openingHours":"Mo-Su 09:00-22:00","foundingDate":"2024"}</script>')


# --------------------------------------------------------------------------- pages
def home():
    P = pfx()
    prods = products()
    feat = "".join(product_card(p) for p in prods[:4])
    imgs = "".join(f'<img src="{P}assets/img/{p["card"]}" alt="{p["name"]}" loading="lazy">' for p in prods[:4])
    services = [
        ("pill", T("Məhsul seçimi", "Product selection", "Подбор продуктов"),
         T("Ürək-damar sağlamlığı, vitaminlər, immunitet və oynaq üçün məhsullar.", "Products for heart health, vitamins, immunity and joints.", "Продукты для здоровья сердца, витамины, иммунитет и суставы.")),
        ("chat", T("Əczaçı məsləhəti", "Pharmacist advice", "Консультация фармацевта"),
         T("Tərkib, doza və saxlanma qaydaları barədə aydın izahat.", "Clear explanations of composition, dosage and storage.", "Понятные объяснения о составе, дозировке и хранении.")),
        ("phone", T("Telefonla sifariş", "Order by phone", "Заказ по телефону"),
         T(f"{PHONE_SHOW} nömrəsinə zəng edərək məhsulu əvvəlcədən ayırdın.", f"Call {PHONE_SHOW} to reserve a product in advance.", f"Позвоните на {PHONE_SHOW}, чтобы заранее зарезервировать товар.")),
        ("shield", T("Təhlükəsizlik", "Safety", "Безопасность"),
         T("Son istifadə tarixi və seriya nömrəsi yoxlanılmış məhsullar.", "Products with checked expiry dates and batch numbers.", "Продукты с проверенными сроками годности и номерами серий.")),
    ]
    sv = "".join(f'<div class="card reveal"><div class="icon">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in services)
    body = head(SITE, T("Kardio Aptek — ürək-damar sağlamlığı, vitaminlər və gündəlik rifah üçün məhsullar, əczaçı məsləhəti. Zəng: ",
                        "Kardio Aptek — products for heart health, vitamins and everyday wellbeing, with pharmacist advice. Call: ",
                        "Kardio Aptek — товары для здоровья сердца, витамины и повседневное благополучие, консультации фармацевта. Телефон: ") + PHONE_SHOW,
                "index.html", jsonld()) + header("index.html", "index.html") + f"""
<section class="hero"><div class="container">
<div><span class="eyebrow">Kardio Aptek · {T('2024-cü ildən', 'since 2024', 'с 2024 года')}</span>
<h1>{T('Ürəyiniz üçün <span>etibarlı</span> ünvan', 'A <span>trusted</span> address for your heart', '<span>Надёжный</span> адрес для вашего сердца')}</h1>
<p class="lead">{T('Keyfiyyətli məhsullar, peşəkar əczaçı məsləhəti və səmimi xidmət — sağlamlığınız üçün hər zaman yanınızdayıq.',
                    'Quality products, professional pharmacist advice and friendly service — we are always by your side for your health.',
                    'Качественные продукты, профессиональные консультации фармацевта и доброжелательный сервис — мы всегда рядом ради вашего здоровья.')}</p>
<div class="actions"><a class="btn btn-primary" href="dermanlar.html">{T('Məhsullara bax', 'View products', 'Смотреть товары')}</a><a class="btn btn-outline" href="tel:{PHONE_RAW}">📞 {PHONE_SHOW}</a></div>
<div class="hero-badges"><span>{T('Tərkibi açıq göstərilir', 'Ingredients clearly listed', 'Состав указан открыто')}</span><span>{T('Peşəkar məsləhət', 'Professional advice', 'Профессиональные советы')}</span><span>{hours()}</span></div></div>
<div class="hero-visual"><div class="stack">{imgs}</div><div class="pulse">{ICON['ecg']} {T('Sağlam ürək — sağlam həyat', 'Healthy heart — healthy life', 'Здоровое сердце — здоровая жизнь')}</div></div>
</div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">{T('Məhsullarımız', 'Our products', 'Наши товары')}</span><h2>{T('Seçilmiş məhsullar', 'Featured products', 'Избранные товары')}</h2>
<p class="lead">{T('Hər məhsulun tərkibi, istifadə qaydası və qablaşdırma şəkilləri ayrıca səhifədə təqdim olunur.',
                    'Each product has its own page with ingredients, directions and packaging photos.',
                    'Для каждого продукта есть отдельная страница с составом, способом применения и фотографиями упаковки.')}</p></div>
<div class="grid g4">{feat}</div>
<p class="center" style="margin-top:28px"><a class="btn btn-green" href="dermanlar.html">{T('Bütün məhsullar →', 'All products →', 'Все товары →')}</a></p>
</div></section>

<section class="section alt"><div class="container">
<div class="section-head center"><span class="eyebrow">{T('Xidmətlər', 'Services', 'Услуги')}</span><h2>{T('Niyə Kardio Aptek?', 'Why Kardio Aptek?', 'Почему Kardio Aptek?')}</h2></div>
<div class="grid g4">{sv}</div></div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">{T('Necə işləyir', 'How it works', 'Как это работает')}</span><h2>{T('Sifariş üç addımda', 'Order in three steps', 'Заказ в три шага')}</h2></div>
<div class="steps">
<div class="step reveal"><h3>{T('Zəng edin', 'Call us', 'Позвоните')}</h3><p>{T(f'{PHONE_SHOW} nömrəsinə zəng edin və ya WhatsApp-da yazın.', f'Call {PHONE_SHOW} or message us on WhatsApp.', f'Позвоните на {PHONE_SHOW} или напишите в WhatsApp.')}</p></div>
<div class="step reveal"><h3>{T('Məsləhət alın', 'Get advice', 'Получите совет')}</h3><p>{T('Əczaçı tərkib və istifadə qaydası barədə məlumat verəcək.', 'A pharmacist will explain the composition and directions for use.', 'Фармацевт расскажет о составе и способе применения.')}</p></div>
<div class="step reveal"><h3>{T('Məhsulu götürün', 'Pick up your product', 'Заберите товар')}</h3><p>{T('Seçdiyiniz məhsulu aptekimizdən əldə edin.', 'Collect your chosen product at our pharmacy.', 'Заберите выбранный товар в нашей аптеке.')}</p></div>
</div></div></section>

<section class="section alt"><div class="container"><div class="notice green reveal"><strong>{T('Vacib məlumat.', 'Important.', 'Важная информация.')}</strong> {T('Saytdakı BAQM (bioloji aktiv qida məhsulu) kateqoriyalı məhsullar dərman vasitəsi deyil, xəstəliklərin müalicəsi məqsədilə istifadə edilməməlidir və normal qidalanmanı əvəz etmir. Hamiləlik, laktasiya, xəstəlik və ya dərman qəbulu zamanı mütləq həkimlə məsləhətləşin.',
 'Products on this site in the dietary supplement (BAQM) category are not medicines, must not be used to treat diseases and do not replace a normal diet. During pregnancy, breastfeeding, illness or when taking medication, always consult a doctor.',
 'Продукты категории БАД (биологически активные добавки) на этом сайте не являются лекарственными средствами, не предназначены для лечения заболеваний и не заменяют полноценное питание. При беременности, кормлении грудью, болезни или приёме лекарств обязательно проконсультируйтесь с врачом.')}</div></div></section>
{cta_block()}""" + footer()
    write("index.html", body)


def about():
    P = pfx()
    prods = products()
    vals = [("heart", T("Qayğı", "Care", "Забота"), T("Hər müştəriyə fərdi yanaşır, sualları səbirlə cavablandırırıq.", "We treat each customer individually and answer questions patiently.", "Мы относимся к каждому клиенту индивидуально и терпеливо отвечаем на вопросы.")),
            ("shield", T("Etibar", "Trust", "Доверие"), T("Tərkibi açıq göstərilən, tarixi və seriyası yoxlanılmış məhsullar təklif edirik.", "We offer products with clearly listed ingredients and checked dates and batches.", "Мы предлагаем продукты с открыто указанным составом и проверенными датами и сериями.")),
            ("book", T("Məlumatlandırma", "Information", "Информирование"), T("Düzgün və anlaşıqlı məlumat — sağlam seçimin əsasıdır.", "Accurate, understandable information is the basis of a healthy choice.", "Точная и понятная информация — основа осознанного выбора."))]
    v = "".join(f'<div class="card reveal"><div class="icon red">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in vals)
    pillars = [
        (T("Şəffaflıq", "Transparency", "Прозрачность"), T("Tərkib, istehsalçı, seriya və tarixlər gizlədilmir — hamısı məhsul səhifəsindədir.", "Ingredients, manufacturer, batch and dates are never hidden — all are on the product page.", "Состав, производитель, серия и даты не скрываются — всё указано на странице товара.")),
        (T("Məsuliyyət", "Responsibility", "Ответственность"), T("BAQM və dərman vasitəsi fərqini aydın bildiririk, həkim məsləhətini əvəz etdiyimizi iddia etmirik.", "We clearly distinguish supplements from medicines and never claim to replace a doctor's advice.", "Мы чётко разделяем БАД и лекарства и не заменяем консультацию врача.")),
        (T("Əlçatanlıq", "Accessibility", "Доступность"), T("Zəng, WhatsApp və ya birbaşa aptekə gələrək suallarınıza cavab ala bilərsiniz.", "Get answers by phone, WhatsApp or by visiting the pharmacy in person.", "Получите ответы по телефону, в WhatsApp или лично в аптеке.")),
        (T("Davamlı inkişaf", "Continuous improvement", "Постоянное развитие"), T("Məhsul çeşidini və xidməti müştəri rəyləri əsasında yaxşılaşdırırıq.", "We improve our range and service based on customer feedback.", "Мы улучшаем ассортимент и сервис на основе отзывов клиентов.")),
    ]
    pl = "".join(f'<div class="pillar reveal"><b>0{i+1}</b><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(pillars))
    promises = T(["Son istifadə tarixi keçmiş məhsul satmırıq", "Məhsulu uyğun şəraitdə saxlayırıq", "Dozanı aşmamaq barədə xəbərdarlıq edirik", "Ciddi hallarda həkimə yönləndiririk"],
                 ["We never sell expired products", "We store products under proper conditions", "We warn against exceeding the dose", "In serious cases we refer you to a doctor"],
                 ["Мы не продаём товары с истёкшим сроком годности", "Мы храним товары в надлежащих условиях", "Мы предупреждаем о недопустимости превышения дозы", "В серьёзных случаях направляем к врачу"])
    pr = "".join(f"<li>{x}</li>" for x in promises)
    body = head(T("Haqqımızda", "About us", "О нас"), T("Kardio Aptek haqqında: missiyamız, dəyərlərimiz və xidmət prinsiplərimiz.", "About Kardio Aptek: our mission, values and service principles.", "О Kardio Aptek: наша миссия, ценности и принципы обслуживания."), "haqqimizda.html") + header("haqqimizda.html", "haqqimizda.html") + page_hero(
        T("Haqqımızda", "About us", "О нас"), T("Kardio Aptek — ürək sağlamlığına və gündəlik rifaha diqqət yetirən müasir apteklərdən biri.", "Kardio Aptek is a modern pharmacy focused on heart health and everyday wellbeing.", "Kardio Aptek — современная аптека, уделяющая внимание здоровью сердца и повседневному благополучию."), [T("Haqqımızda", "About us", "О нас")]) + f"""
<section class="section"><div class="container grid g2" style="align-items:center;gap:44px">
<div class="reveal"><span class="eyebrow">{T('Biz kimik', 'Who we are', 'Кто мы')}</span><h2>{T('Ürək sağlamlığına diqqət edən müasir aptek', 'A modern pharmacy that cares about heart health', 'Современная аптека, заботящаяся о здоровье сердца')}</h2>
<p>{T(f'Kardio Aptek {YEAR}-cü ildə Bakıda, Qara Qarayev metrostansiyasının yaxınlığında fəaliyyətə başlayıb. Məqsədimiz hər müştəriyə rahat, etibarlı və anlaşıqlı xidmət göstərməkdir.',
      f'Kardio Aptek opened in {YEAR} in Baku, near Qara Qarayev metro station. Our goal is to give every customer convenient, reliable and clear service.',
      f'Kardio Aptek открылась в {YEAR} году в Баку, рядом со станцией метро «Гара Гараев». Наша цель — удобное, надёжное и понятное обслуживание каждого клиента.')}</p>
<p>{T('Təklif etdiyimiz hər məhsul üçün tərkib, doza, istehsalçı və son istifadə tarixi açıq şəkildə göstərilir. Saytdakı məhsul səhifələrində qablaşdırma şəkilləri və tərkib cədvəli də yerləşdirilib ki, qərarı məlumatlı şəkildə verəsiniz.',
      'For every product we offer, the composition, dosage, manufacturer and expiry date are clearly shown. Product pages on this site also include packaging photos and an ingredient table so you can decide with confidence.',
      'Для каждого продукта открыто указаны состав, дозировка, производитель и срок годности. На страницах товаров размещены фотографии упаковки и таблица состава, чтобы вы могли принять взвешенное решение.')}</p>
<a class="btn btn-green" href="dermanlar.html">{T('Məhsullarımıza baxın', 'See our products', 'Смотреть товары')}</a></div>
<div class="reveal"><div class="card" style="padding:12px;background:var(--green-soft)"><div class="grid g2" style="gap:10px">
{"".join(f'<img src="{P}assets/img/{p["card"]}" alt="{p["name"]}" style="background:#fff;border-radius:12px;aspect-ratio:1;object-fit:contain;padding:6px" loading="lazy">' for p in prods[:4])}
</div></div></div></div></section>

<section class="section alt"><div class="container"><div class="section-head center"><span class="eyebrow">{T('Dəyərlərimiz', 'Our values', 'Наши ценности')}</span><h2>{T('Nəyə əsaslanırıq', 'What we stand for', 'На чём мы стоим')}</h2></div>
<div class="grid g3">{v}</div></div></section>

<section class="section"><div class="container">
<div class="section-head center"><span class="eyebrow">{T('Missiya və baxış', 'Mission & vision', 'Миссия и видение')}</span><h2>{T('Hara getdiyimizi bilirik', 'We know where we are heading', 'Мы знаем, куда идём')}</h2></div>
<div class="mv">
<div class="mv-card mission reveal"><span class="mv-ico">{ICON['heart']}</span><h3>{T('Missiyamız', 'Our mission', 'Наша миссия')}</h3>
<p>{T('Hər kəsin sağlamlıq barədə düzgün məlumata və keyfiyyətli məhsullara rahat çıxışını təmin etmək; müştərini məlumatlı seçim etməyə yönəltmək.',
     'To give everyone easy access to accurate health information and quality products, and to help customers make informed choices.',
     'Обеспечить каждому удобный доступ к достоверной информации о здоровье и качественным продуктам, помогая делать осознанный выбор.')}</p></div>
<div class="mv-card vision reveal"><span class="mv-ico">{ICON['ecg']}</span><h3>{T('Baxışımız', 'Our vision', 'Наше видение')}</h3>
<p>{T('Ürək-damar sağlamlığı və gündəlik rifah sahəsində Bakıda ən çox güvənilən apteklərdən birinə çevrilmək.',
     'To become one of the most trusted pharmacies in Baku for cardiovascular health and everyday wellbeing.',
     'Стать одной из самых надёжных аптек Баку в области здоровья сердца и сосудов и повседневного благополучия.')}</p></div></div>
<div class="pillars">{pl}</div>
<div class="promise reveal"><div><h3>{T('Bizim sözümüz', 'Our promise', 'Наше обещание')}</h3><p>{T('Hər müştəriyə eyni hörmət, hər sualına dürüst cavab.', 'The same respect for every customer, an honest answer to every question.', 'Одинаковое уважение к каждому клиенту и честный ответ на каждый вопрос.')}</p></div>
<ul>{pr}</ul></div>
</div></section>
{cta_block()}""" + footer()
    write("haqqimizda.html", body)


def catalog():
    chips = "".join(f'<button class="chip{" active" if k == "all" else ""}" data-filter="{k}" type="button">{t}</button>' for k, t in cats())
    cards = "".join(product_card(p) for p in products())
    ttl = T("Dərmanlar və sağlamlıq məhsulları", "Medicines & health products", "Препараты и товары для здоровья")
    body = head(T("Dərmanlar", "Medicines", "Препараты"), T("Kardio Aptek məhsulları: Karno Mer, Depomer D3+K2, Revimer, Chondramer — tərkib, doza və qablaşdırma şəkilləri.",
                                                         "Kardio Aptek products: Karno Mer, Depomer D3+K2, Revimer, Chondramer — ingredients, dosage and packaging photos.",
                                                         "Товары Kardio Aptek: Karno Mer, Depomer D3+K2, Revimer, Chondramer — состав, дозировка и фотографии упаковки."), "dermanlar.html") + header("dermanlar.html", "dermanlar.html") + page_hero(
        ttl, T("Hər məhsulun tərkibi, istifadə qaydası və qablaşdırma şəkilləri ilə tanış olun.", "Explore each product's ingredients, directions and packaging photos.", "Ознакомьтесь с составом, способом применения и фото упаковки каждого товара."), [T("Dərmanlar", "Medicines", "Препараты")]) + f"""
<section class="section"><div class="container">
<div class="notice reveal" style="margin-bottom:28px"><strong>{T('Diqqət:', 'Please note:', 'Внимание:')}</strong> {T('Aşağıdakı məhsullar BAQM (bioloji aktiv qida məhsulu) və ya tibbi vasitədir — <strong>dərman vasitəsi deyil</strong>. Xəstəliklərin müalicəsi məqsədilə istifadə edilməməlidir. İstifadədən əvvəl həkimlə məsləhətləşin.',
 'The products below are dietary supplements (BAQM) or a medical device — <strong>not medicines</strong>. They must not be used to treat diseases. Consult a doctor before use.',
 'Представленные ниже товары являются БАД или медицинским изделием — <strong>не лекарственными средствами</strong>. Они не предназначены для лечения заболеваний. Перед применением проконсультируйтесь с врачом.')}</div>
<div class="toolbar"><div class="chips" role="group">{chips}</div>
<input id="q" class="search" type="search" placeholder="{T('Məhsul axtar…', 'Search products…', 'Поиск товаров…')}" aria-label="{T('Məhsul axtar', 'Search products', 'Поиск товаров')}"></div>
<div class="grid g4">{cards}</div>
<p class="empty">{T('Axtarışa uyğun məhsul tapılmadı. Zəng edin:', 'No matching products found. Call us:', 'Ничего не найдено. Позвоните нам:')} <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></p>
</div></section>{cta_block()}""" + footer()
    write("dermanlar.html", body)


def li(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def detail(p):
    P = pfx()
    # small line: for az/ru show the English name; for en show the Latin/INCI name when different
    rows = ""
    for nm, sm, c in p["ing"]:
        main = nm[LANGS.index(LANG)]
        small = nm[1] if LANG != "en" else (sm if sm.lower() != main.lower() else "")
        small_html = f"<small>{e(small)}</small>" if small and small != main else ""
        rows += f"<tr><td>{e(main)}{small_html}</td><td>{e(units(c))}</td></tr>"
    gal = "".join(
        f'<button class="shot" type="button" data-full="{P}assets/img/{f}" data-cap="{e(c)}"><img src="{P}assets/img/{f}" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></button>'
        for f, c in p["gallery"])
    ids = []
    if p["reg"]:
        ids.append(f"{T('Qeydiyyat №', 'Registration no.', 'Рег. №')}: {p['reg']}")
    if p["extra"]:
        ids.append(p["extra"])
    ids_html = f'<li>{e(" · ".join(ids))}</li>' if ids else ""
    parts = []
    if p["series"]:
        parts.append(f"<b>{T('Seriya', 'Batch', 'Серия')}:</b> {p['series']}")
    if p["made"]:
        parts.append(f"<b>{T('İstehsal', 'Produced', 'Произведено')}:</b> {p['made']}")
    if p["exp"]:
        parts.append(f"<b>{T('Son istifadə', 'Expires', 'Годен до')}:</b> {p['exp']}")
    batch_html = f"<li>{' · '.join(parts)}</li>" if parts else ""
    about_html = f'<div class="info-block"><h3>{T("Məhsul haqqında", "About the product", "О продукте")}</h3><p>{p["about"]}</p></div>' if p.get("about") else ""
    uses_html = f'<div class="info-block"><h3>{T("İstifadə sahəsi", "Areas of use", "Область применения")}</h3>{li(p["uses"])}</div>' if p.get("uses") else ""
    rest = [o for o in products() if o["slug"] != p["slug"]]
    rest.sort(key=lambda o: o["cat"] != p["cat"])
    others = "".join(product_card(o) for o in rest[:3])
    warn = (T("Tibbi vasitədir, dərman vasitəsi deyil.", "A medical device, not a medicine.", "Медицинское изделие, не лекарственное средство.") if p["medical"]
            else T("Dərman vasitəsi deyil. Bioloji aktiv qida məhsuludur.", "Not a medicine. A dietary supplement.", "Не является лекарственным средством. Биологически активная добавка."))
    crumb = f'<a href="dermanlar.html">{T("Dərmanlar", "Medicines", "Препараты")}</a>'
    body = head(p["name"], f"{p['name']} — {p['short']} " + T("Tərkib, doza və əks göstərişlər.", "Ingredients, dosage and contraindications.", "Состав, дозировка и противопоказания."),
                f"derman-{p['slug']}.html") + header("dermanlar.html", f"derman-{p['slug']}.html") + page_hero(p["name"], p["short"], [crumb, p["name"]]) + f"""
<section class="section"><div class="container">
<div class="detail">
<div class="reveal"><div class="main-img"><img src="{P}assets/img/{p['head']}" alt="{p['name']}"></div>
<p style="margin-top:14px"><a class="btn btn-primary" href="tel:{PHONE_RAW}">📞 {T('Sifariş', 'Order', 'Заказ')}: {PHONE_SHOW}</a></p></div>
<div class="reveal">
<span class="tag {'red' if p['medical'] else ''}">{p['kind']}</span>
<h2 style="margin-top:10px">{p['name']}</h2>
<p class="lead" style="font-size:1rem">{p['indication']}</p>
<div class="facts">
<div class="fact"><small>{T('Buraxılış forması', 'Dosage form', 'Форма выпуска')}</small><b>{p['form']}</b></div>
<div class="fact"><small>{T('Qablaşdırma', 'Packaging', 'Упаковка')}</small><b>{p['pack']}</b></div>
<div class="fact"><small>{T('Aptekdən buraxılma', 'Pharmacy dispensing', 'Условия отпуска')}</small><b>{rx()}</b></div>
<div class="fact"><small>{T('Yararlılıq müddəti', 'Shelf life', 'Срок годности')}</small><b>{p['shelf']}</b></div></div>

{about_html}{uses_html}
<div class="info-block"><h3>{T('Tərkibi', 'Ingredients', 'Состав')}</h3>
<table class="ing"><caption style="caption-side:top;padding-bottom:8px">{p['comp_title']}</caption><thead><tr><th>{T('Maddə', 'Ingredient', 'Вещество')}</th><th style="text-align:right">{T('Miqdar', 'Amount', 'Количество')}</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="info-block"><h3>{T('Köməkçi maddələr', 'Excipients', 'Вспомогательные вещества')}</h3><p>{p['excip']}</p></div>
<div class="info-block"><h3>{T('İstifadə qaydası və doza', 'Directions and dosage', 'Способ применения и дозировка')}</h3>{li(p['dose'])}</div>
<div class="info-block"><h3>{T('Əks göstərişlər', 'Contraindications', 'Противопоказания')}</h3>{li(p['contra'])}</div>
<div class="info-block"><h3>{T('Saxlanma şəraiti', 'Storage conditions', 'Условия хранения')}</h3><p>{p['storage']}</p></div>
<div class="info-block"><h3>{T('İstehsalçı və məlumatlar', 'Manufacturer & details', 'Производитель и данные')}</h3><ul>
<li><b>{T('İstehsalçı', 'Manufacturer', 'Производитель')}:</b> {e(p['mfr'])}</li><li><b>{T('Ticarət nişanı', 'Trademark', 'Торговая марка')}:</b> {e(p['brand'])}</li>
{batch_html}{ids_html}</ul></div>

<div class="notice" style="margin-top:26px"><strong>{warn}</strong>
{T('Tövsiyə edilən sutkalıq dozanı keçməyin. Uşaqların əli çatmayan yerdə saxlayın. Hamiləlik və laktasiya dövründə, xəstəlik və ya dərman istifadəsi zamanı həkimlə məsləhətləşin.',
   'Do not exceed the recommended daily dose. Keep out of reach of children. During pregnancy and breastfeeding, illness or while taking medication, consult a doctor.',
   'Не превышайте рекомендуемую суточную дозу. Храните в недоступном для детей месте. При беременности и кормлении грудью, болезни или приёме лекарств проконсультируйтесь с врачом.')}</div>
</div></div></div></section>

<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">{T('Qablaşdırma', 'Packaging', 'Упаковка')}</span><h2>{p['name']} — {T('qablaşdırma şəkilləri', 'packaging photos', 'фотографии упаковки')}</h2>
<p class="lead">{T('Şəkli böyütmək üçün üzərinə klikləyin.', 'Click a photo to enlarge it.', 'Нажмите на фото, чтобы увеличить.')}</p></div><div class="gallery">{gal}</div></div></section>

<section class="section"><div class="container"><div class="section-head"><h2>{T('Digər məhsullar', 'Other products', 'Другие товары')}</h2></div><div class="grid g3">{others}</div></div></section>""" + footer()
    write(f"derman-{p['slug']}.html", body)


def services():
    items = [
        ("pill", T("Məhsul satışı", "Product sales", "Продажа товаров"), T("Ürək-damar sağlamlığı, vitamin, immunitet və oynaq üçün məhsullar.", "Products for heart health, vitamins, immunity and joints.", "Продукты для здоровья сердца, витамины, иммунитет и суставы.")),
        ("chat", T("Əczaçı məsləhəti", "Pharmacist advice", "Консультация фармацевта"), T("Məhsulun tərkibi, dozası, saxlanması və əks göstərişləri barədə məlumat.", "Information on composition, dosage, storage and contraindications.", "Информация о составе, дозировке, хранении и противопоказаниях.")),
        ("phone", T("Telefonla sifariş", "Order by phone", "Заказ по телефону"), T(f"{PHONE_SHOW} nömrəsinə zəng və ya WhatsApp vasitəsilə məhsulun mövcudluğunu öyrənin.", f"Check availability by calling {PHONE_SHOW} or writing on WhatsApp.", f"Узнайте о наличии, позвонив на {PHONE_SHOW} или написав в WhatsApp.")),
        ("clock", T("Tarixlərin yoxlanması", "Date checks", "Проверка сроков"), T("Təqdim olunan məhsulların seriya və son istifadə tarixi diqqətlə yoxlanılır.", "Batch numbers and expiry dates of our products are carefully checked.", "Номера серий и сроки годности наших товаров тщательно проверяются.")),
        ("ecg", T("Ürək sağlamlığı məlumatı", "Heart-health information", "Информация о здоровье сердца"), T("Həyat tərzi və qidalanma üzrə ümumi məlumat materialları.", "General information on lifestyle and nutrition.", "Общие информационные материалы об образе жизни и питании.")),
        ("drop", T("Düzgün saxlama tövsiyələri", "Storage guidance", "Рекомендации по хранению"), T("Məhsulların temperatur və rütubət şərtlərinə uyğun saxlanması barədə təlimat.", "Guidance on storing products according to temperature and humidity requirements.", "Рекомендации по хранению товаров с учётом температуры и влажности.")),
    ]
    cards = "".join(f'<div class="card reveal"><div class="icon">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)
    ttl = T("Xidmətlər", "Services", "Услуги")
    body = head(ttl, T("Kardio Aptek xidmətləri: məhsul satışı, əczaçı məsləhəti, telefonla sifariş.", "Kardio Aptek services: product sales, pharmacist advice, phone orders.", "Услуги Kardio Aptek: продажа товаров, консультации фармацевта, заказ по телефону."), "xidmetler.html") + header("xidmetler.html", "xidmetler.html") + page_hero(
        T("Xidmətlərimiz", "Our services", "Наши услуги"), T("Sizə rahat və etibarlı xidmət göstərmək üçün buradayıq.", "We are here to give you convenient and reliable service.", "Мы здесь, чтобы предложить вам удобный и надёжный сервис."), [ttl]) + f"""
<section class="section"><div class="container"><div class="grid g3">{cards}</div></div></section>
<section class="section alt"><div class="container"><div class="notice green reveal"><strong>{T('Qeyd:', 'Note:', 'Примечание:')}</strong> {T('Əczaçı məsləhəti məlumat xarakterlidir və həkimin diaqnoz və müalicəsini əvəz etmir. Ciddi şikayətlər zamanı həkimə müraciət edin.',
 "A pharmacist's advice is informational and does not replace a doctor's diagnosis or treatment. See a doctor for serious complaints.",
 'Консультация фармацевта носит информационный характер и не заменяет диагностику и лечение у врача. При серьёзных жалобах обратитесь к врачу.')}</div></div></section>
{cta_block()}""" + footer()
    write("xidmetler.html", body)


def tips():
    tp = [
        (T("Duz və doymuş yağları azaldın", "Cut down on salt and saturated fat", "Сократите соль и насыщенные жиры"),
         T("Gündəlik duz qəbulunu məhdudlaşdırmaq qan təzyiqinə nəzarət üçün vacibdir. Tərəvəz, meyvə, bütövdənli məhsullar və balıq daha yaxşı seçimdir.",
           "Limiting daily salt intake helps control blood pressure. Vegetables, fruit, whole grains and fish are better choices.",
           "Ограничение соли помогает контролировать артериальное давление. Лучше выбирать овощи, фрукты, цельнозерновые продукты и рыбу.")),
        (T("Hərəkət edin", "Stay active", "Двигайтесь"),
         T("Həftədə ən azı 150 dəqiqə orta intensivlikli fiziki fəaliyyət (sürətli yeriş, üzgüçülük) ürək-damar sağlamlığına dəstək olur.",
           "At least 150 minutes of moderate physical activity a week (brisk walking, swimming) supports cardiovascular health.",
           "Не менее 150 минут умеренной физической активности в неделю (быстрая ходьба, плавание) поддерживает здоровье сердца и сосудов.")),
        (T("Siqaretdən imtina edin", "Quit smoking", "Откажитесь от курения"),
         T("Siqaret ürək-damar xəstəlikləri üçün əsas risk amillərindən biridir. İmtina etmək üçün həkimdən kömək ala bilərsiniz.",
           "Smoking is one of the main risk factors for cardiovascular disease. A doctor can help you quit.",
           "Курение — один из главных факторов риска сердечно-сосудистых заболеваний. Врач поможет вам бросить.")),
        (T("Təzyiqi və çəkini izləyin", "Monitor blood pressure and weight", "Следите за давлением и весом"),
         T("Qan təzyiqini müntəzəm ölçün, normal bədən çəkisini qoruyun və həkim yoxlamalarını buraxmayın.",
           "Measure blood pressure regularly, maintain a healthy weight and keep up with check-ups.",
           "Регулярно измеряйте давление, поддерживайте нормальный вес и не пропускайте плановые осмотры.")),
        (T("Keyfiyyətli yuxu və stress idarəsi", "Good sleep and stress management", "Качественный сон и управление стрессом"),
         T("Gündə 7–8 saat yuxu və stressi azaldan vərdişlər (gəzinti, nəfəs məşqləri) ümumi sağlamlığa müsbət təsir edir.",
           "7–8 hours of sleep and stress-reducing habits (walks, breathing exercises) benefit overall health.",
           "7–8 часов сна и привычки, снижающие стресс (прогулки, дыхательные упражнения), положительно влияют на здоровье.")),
        (T("Vitamin və əlavələri düşünərək seçin", "Choose vitamins and supplements wisely", "Осознанно выбирайте витамины и добавки"),
         T("Vitamin və BAQM-lar tarazlı qidalanmanı əvəz etmir. D vitamini kimi məhsulları qəbul etməzdən əvvəl dozanı həkimlə razılaşdırın.",
           "Vitamins and supplements do not replace a balanced diet. Agree the dose with your doctor before taking products such as vitamin D.",
           "Витамины и БАД не заменяют сбалансированное питание. Перед приёмом, например, витамина D согласуйте дозу с врачом.")),
    ]
    t = "".join(f'<div class="card tip reveal"><div class="num">{i+1}</div><div><h3>{a}</h3><p>{b}</p></div></div>' for i, (a, b) in enumerate(tp))
    ttl = T("Sağlamlıq məsləhətləri", "Health tips", "Советы по здоровью")
    body = head(ttl, T("Ürək sağlamlığı üçün ümumi məsləhətlər: qidalanma, hərəkət, təzyiqə nəzarət və vitaminlərə düzgün yanaşma.",
                       "General heart-health tips: nutrition, activity, blood-pressure control and a sensible approach to vitamins.",
                       "Общие советы для здоровья сердца: питание, активность, контроль давления и разумный подход к витаминам."), "meslehetler.html") + header("meslehetler.html", "meslehetler.html") + page_hero(
        ttl, T("Ürək sağlamlığı və gündəlik rifah üçün sadə, ümumi tövsiyələr.", "Simple, general recommendations for heart health and everyday wellbeing.", "Простые общие рекомендации для здоровья сердца и повседневного благополучия."), [T("Məsləhətlər", "Tips", "Советы")]) + f"""
<section class="section"><div class="container"><div class="grid g2">{t}</div>
<div class="notice reveal" style="margin-top:28px"><strong>{T('Xəbərdarlıq:', 'Warning:', 'Предупреждение:')}</strong> {T('Bu səhifədəki məlumatlar ümumi xarakter daşıyır və fərdi tibbi məsləhəti əvəz etmir. Sinə ağrısı, nəfəs darlığı, huşun itməsi kimi hallarda dərhal təcili yardım çağırın.',
 'The information on this page is general and does not replace personalised medical advice. In case of chest pain, shortness of breath or loss of consciousness, call emergency services immediately.',
 'Информация на этой странице носит общий характер и не заменяет индивидуальную медицинскую консультацию. При боли в груди, одышке или потере сознания немедленно вызывайте скорую помощь.')}</div></div></section>
{cta_block()}""" + footer()
    write("meslehetler.html", body)


def faq():
    qa = [
        (T("BAQM nədir?", "What is a dietary supplement (BAQM)?", "Что такое БАД?"),
         T("BAQM — bioloji aktiv qida məhsulu deməkdir. Bu məhsullar dərman vasitəsi deyil; qidaya əlavə kimi nəzərdə tutulub və xəstəliklərin müalicəsi üçün istifadə edilməməlidir.",
           "BAQM stands for biologically active food product. These are not medicines; they are intended as a supplement to the diet and must not be used to treat diseases.",
           "БАД — биологически активная добавка к пище. Это не лекарственные средства; они предназначены для дополнения рациона и не должны использоваться для лечения заболеваний.")),
        (T("Məhsulları reseptsiz almaq olarmı?", "Can I buy the products without a prescription?", "Можно ли купить товары без рецепта?"),
         T("Saytda təqdim olunan məhsulların hamısı aptekdən reseptsiz buraxılır. Yenə də istifadədən əvvəl həkim və ya əczaçı ilə məsləhətləşməyiniz tövsiyə olunur.",
           "All products on this site are dispensed without a prescription. Still, it is recommended to consult a doctor or pharmacist before use.",
           "Все товары на сайте отпускаются без рецепта. Тем не менее перед применением рекомендуется проконсультироваться с врачом или фармацевтом.")),
        (T("Hamiləlik və ya əmizdirmə dövründə istifadə edə bilərəmmi?", "Can I use them during pregnancy or breastfeeding?", "Можно ли применять при беременности и кормлении грудью?"),
         T("Məhsulların etiketində göstərildiyi kimi, hamiləlik və laktasiya dövründə, həmçinin xəstəlik və ya dərman qəbulu zamanı mütləq həkimlə məsləhətləşin.",
           "As stated on the product labels, always consult a doctor during pregnancy and lactation, as well as during illness or when taking medication.",
           "Как указано на этикетках, при беременности и лактации, а также при болезни или приёме лекарств обязательно проконсультируйтесь с врачом.")),
        (T("Uşaqlar üçün uyğundurmu?", "Are they suitable for children?", "Подходят ли они детям?"),
         T("Depomer D3+K2 etiketdə 2–4 və 4–14 yaş qrupları üçün uyğun göstərilib. Digər məhsullar üçün həkim məsləhəti lazımdır. Bütün məhsulları uşaqların əli çatmayan yerdə saxlayın.",
           "Depomer D3+K2 is labelled as suitable for the 2–4 and 4–14 age groups. For other products a doctor's advice is needed. Keep all products out of reach of children.",
           "Depomer D3+K2 на этикетке указан как подходящий для возрастных групп 2–4 и 4–14 лет. Для остальных товаров нужна консультация врача. Храните все товары в недоступном для детей месте.")),
        (T("Məhsulları necə saxlamalıyam?", "How should I store the products?", "Как хранить товары?"),
         T("Etiketlərə əsasən 25 °C-dən yüksək olmayan temperaturda, quru, işıqdan qorunan və uşaqların əli çatmayan yerdə saxlayın.",
           "According to the labels, store at a temperature not above 25 °C, in a dry place protected from light and out of reach of children.",
           "Согласно этикеткам, храните при температуре не выше 25 °C, в сухом, защищённом от света и недоступном для детей месте.")),
        (T("Yararlılıq müddəti nə qədərdir?", "What is the shelf life?", "Каков срок годности?"),
         T("Təqdim etdiyimiz məhsulların yararlılıq müddəti istehsal tarixindən 3 ildir. Tarix qutunun üzərində göstərilir; müddət bitdikdən sonra istifadə etməyin.",
           "The shelf life of our products is 3 years from the production date. The date is printed on the box; do not use after it expires.",
           "Срок годности наших товаров — 3 года с даты производства. Дата указана на коробке; по истечении срока не используйте.")),
        (T("Məhsulu necə sifariş edə bilərəm?", "How can I order a product?", "Как заказать товар?"),
         T(f"{PHONE_SHOW} nömrəsinə zəng edin, WhatsApp-da yazın və ya Əlaqə səhifəsindəki formadan istifadə edin.",
           f"Call {PHONE_SHOW}, message us on WhatsApp or use the form on the Contact page.",
           f"Позвоните на {PHONE_SHOW}, напишите в WhatsApp или воспользуйтесь формой на странице «Контакты».")),
        (T("Dozanı artırsam daha tez təsir edərmi?", "Will a higher dose work faster?", "Подействует ли быстрее увеличенная доза?"),
         T("Xeyr. Tövsiyə edilən sutkalıq dozanı keçməyin. Dozanın dəyişdirilməsi yalnız həkim məsləhəti ilə mümkündür.",
           "No. Do not exceed the recommended daily dose. The dose may only be changed on a doctor's advice.",
           "Нет. Не превышайте рекомендуемую суточную дозу. Изменять дозу можно только по рекомендации врача.")),
    ]
    d = "".join(f"<details class='reveal'><summary>{q}</summary><p>{a}</p></details>" for q, a in qa)
    ttl = T("Tez-tez verilən suallar", "Frequently asked questions", "Часто задаваемые вопросы")
    body = head(ttl, T("Kardio Aptek: BAQM, doza, saxlanma, yararlılıq müddəti və sifariş barədə tez-tez verilən suallar.",
                       "Kardio Aptek: frequently asked questions about supplements, dosage, storage, shelf life and ordering.",
                       "Kardio Aptek: ответы на частые вопросы о БАД, дозировке, хранении, сроке годности и заказе."), "suallar.html") + header("suallar.html", "suallar.html") + page_hero(
        ttl, T("Ən çox soruşulan suallara qısa cavablar.", "Short answers to the most common questions.", "Краткие ответы на самые частые вопросы."), [T("Suallar", "FAQ", "Вопросы")]) + f"""
<section class="section"><div class="container" style="max-width:820px">{d}</div></section>{cta_block()}""" + footer()
    write("suallar.html", body)


def contact():
    ttl = T("Əlaqə", "Contact", "Контакты")
    tpl = f'data-t1="{T("Salam! Mən ", "Hello! My name is ", "Здравствуйте! Меня зовут ")}" data-t2="{T("Telefon", "Phone", "Телефон")}" data-t3="{T("Mövzu", "Topic", "Тема")}"'
    body = head(ttl, T(f"Kardio Aptek ilə əlaqə: {PHONE_SHOW}. WhatsApp və ya zəng ilə sifariş və məsləhət.", f"Contact Kardio Aptek: {PHONE_SHOW}. Orders and advice by phone or WhatsApp.", f"Связаться с Kardio Aptek: {PHONE_SHOW}. Заказы и консультации по телефону или в WhatsApp."), "elaqe.html") + header("elaqe.html", "elaqe.html") + page_hero(
        ttl, T("Sualınız və ya sifarişiniz üçün bizimlə əlaqə saxlayın.", "Get in touch for questions or orders.", "Свяжитесь с нами по вопросам или для заказа."), [ttl]) + f"""
<section class="section"><div class="container contact-grid">
<div class="reveal"><ul class="contact-list">
<li><div class="icon red">{ICON['phone']}</div><div><small>{T('Telefon', 'Phone', 'Телефон')}</small><b><a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a></b></div></li>
<li><div class="icon">{ICON['wa']}</div><div><small>WhatsApp</small><b><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{T('Mesaj yazın', 'Send a message', 'Написать сообщение')}</a></b></div></li>
<li><div class="icon">{ICON['pin']}</div><div><small>{T('Ünvan', 'Address', 'Адрес')}</small><b>{city()}</b></div></li>
<li><div class="icon">{ICON['clock']}</div><div><small>{T('İş saatları', 'Opening hours', 'Часы работы')}</small><b>{hours()}</b></div></li></ul></div>
<div class="card reveal"><h3>{T('Bizə yazın', 'Write to us', 'Напишите нам')}</h3><p style="margin-bottom:16px">{T('Formu doldurduqda mesajınız WhatsApp-da hazır şəkildə açılacaq.', 'When you submit the form, your message opens ready to send in WhatsApp.', 'После отправки формы сообщение откроется в WhatsApp уже готовым к отправке.')}</p>
<form id="contact-form" data-wa="{WA}" {tpl}>
<label for="n">{T('Adınız', 'Your name', 'Ваше имя')}</label><input class="input" id="n" name="name" required autocomplete="name">
<label for="p">{T('Telefon', 'Phone', 'Телефон')}</label><input class="input" id="p" name="phone" type="tel" required autocomplete="tel">
<label for="t">{T('Mövzu', 'Topic', 'Тема')}</label><select class="input" id="t" name="topic"><option>{T('Məhsul haqqında sual', 'Question about a product', 'Вопрос о товаре')}</option><option>{T('Sifariş', 'Order', 'Заказ')}</option><option>{T('Digər', 'Other', 'Другое')}</option></select>
<label for="m">{T('Mesaj', 'Message', 'Сообщение')}</label><textarea class="input" id="m" name="message" required></textarea>
<button class="btn btn-primary" type="submit">{T('WhatsApp-da göndər', 'Send via WhatsApp', 'Отправить в WhatsApp')}</button></form></div>
</div></section>
<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">{T('Xəritə', 'Map', 'Карта')}</span><h2>{T('Bizi necə tapmaq olar', 'How to find us', 'Как нас найти')}</h2>
<p class="lead">{T('Qara Qarayev metrostansiyasının yaxınlığında, S. Mirzəyev küçəsində yerləşirik.', 'We are located near Qara Qarayev metro station, on S. Mirzayev street.', 'Мы находимся рядом со станцией метро «Гара Гараев», на улице С. Мирзоева.')}</p></div>
<div class="map reveal"><iframe title="Kardio Aptek — Google Maps" src="{map_embed()}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<p style="margin-top:18px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="{MAP_DIR}" target="_blank" rel="noopener">📍 {T('Yol tarifi al', 'Get directions', 'Построить маршрут')}</a><a class="btn btn-outline" href="{MAP_LINK}" target="_blank" rel="noopener">{T('Google Maps-də aç', 'Open in Google Maps', 'Открыть в Google Maps')}</a></p></div></section>""" + footer()
    write("elaqe.html", body)


def privacy():
    ttl = T("Məxfilik siyasəti", "Privacy policy", "Политика конфиденциальности")
    body = head(ttl, T("Kardio Aptek saytının məxfilik siyasəti.", "Privacy policy of the Kardio Aptek website.", "Политика конфиденциальности сайта Kardio Aptek."), "mexfiyyet.html") + header("", "mexfiyyet.html") + page_hero(
        ttl, T(f"Son yenilənmə: {YEAR}", f"Last updated: {YEAR}", f"Последнее обновление: {YEAR}"), [T("Məxfilik", "Privacy", "Конфиденциальность")]) + f"""
<section class="section"><div class="container prose">
<h2>{T('Toplanan məlumatlar', 'Data we collect', 'Собираемые данные')}</h2><p>{T('Bu sayt serverdə şəxsi məlumat saxlamır. Əlaqə formasında daxil etdiyiniz məlumatlar (ad, telefon, mesaj) yalnız sizin təsdiqinizlə WhatsApp vasitəsilə bizə göndərilir.',
 'This site does not store personal data on a server. Information you enter in the contact form (name, phone, message) is sent to us via WhatsApp only with your confirmation.',
 'Этот сайт не хранит персональные данные на сервере. Данные, введённые в форме обратной связи (имя, телефон, сообщение), отправляются нам через WhatsApp только с вашего подтверждения.')}</p>
<h2>{T('Üçüncü tərəflər', 'Third parties', 'Третьи стороны')}</h2><p>{T('Sayt şrift yükləmək üçün Google Fonts, xəritə üçün isə Google Maps xidmətindən istifadə edir; bu zaman brauzeriniz həmin xidmətlərə sorğu göndərir.',
 'The site uses Google Fonts to load fonts and Google Maps for the map; your browser sends requests to these services.',
 'Сайт использует Google Fonts для загрузки шрифтов и Google Maps для карты; при этом ваш браузер отправляет запросы к этим сервисам.')}</p>
<h2>{T('Tibbi məlumat', 'Medical information', 'Медицинская информация')}</h2><p>{T('Saytdakı məlumatlar məlumat xarakterlidir, həkim məsləhətini və diaqnozu əvəz etmir.', 'The information on this site is for reference only and does not replace medical advice or diagnosis.', 'Информация на сайте носит справочный характер и не заменяет консультацию врача и диагностику.')}</p>
<h2>{T('Əlaqə', 'Contact', 'Контакты')}</h2><p>{T('Suallarınız üçün', 'For any questions', 'По всем вопросам')}: <a href="tel:{PHONE_RAW}">{PHONE_SHOW}</a>.</p></div></section>""" + footer()
    write("mexfiyyet.html", body)


def not_found():
    ttl = T("Səhifə tapılmadı", "Page not found", "Страница не найдена")
    body = head(ttl, T("Axtardığınız səhifə mövcud deyil.", "The page you are looking for does not exist.", "Запрашиваемая страница не существует."), "404.html") + header("", "404.html") + f"""
<section class="section"><div class="container center"><span class="eyebrow">404</span><h1>{ttl}</h1>
<p class="lead">{T('Axtardığınız səhifə köçürülüb və ya mövcud deyil.', 'The page you are looking for has moved or does not exist.', 'Страница перемещена или не существует.')}</p><p><a class="btn btn-green" href="index.html">{T('Ana səhifəyə qayıt', 'Back to home', 'На главную')}</a></p></div></section>""" + footer()
    write("404.html", body)


def static():
    (ROOT / "favicon.svg").write_text(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1), encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    # root redirect for 404 asset paths is not needed; language folders reference ../assets


if __name__ == "__main__":
    for LANG in LANGS:
        home(); about(); catalog()
        for p in products():
            detail(p)
        services(); tips(); faq(); contact(); privacy(); not_found()
    static()
