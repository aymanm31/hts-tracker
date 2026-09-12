# maps HTS chapter number (as int) to (section_roman_numeral, section_name)
CHAPTER_TO_SECTION = {}

_SECTIONS = [
    ("I", "Live Animals; Animal Products", range(1, 6)),
    ("II", "Vegetable Products", range(6, 15)),
    ("III", "Animal or Vegetable Fats and Oils", range(15, 16)),
    ("IV", "Prepared Foodstuffs; Beverages; Tobacco", range(16, 25)),
    ("V", "Mineral Products", range(25, 28)),
    ("VI", "Products of the Chemical or Allied Industries", range(28, 39)),
    ("VII", "Plastics and Rubber", range(39, 41)),
    ("VIII", "Raw Hides, Leather, Furskins", range(41, 44)),
    ("IX", "Wood and Articles of Wood", range(44, 47)),
    ("X", "Pulp, Paper", range(47, 50)),
    ("XI", "Textiles and Textile Articles", range(50, 64)),
    ("XII", "Footwear, Headgear, Umbrellas", range(64, 68)),
    ("XIII", "Articles of Stone, Ceramic, Glass", range(68, 71)),
    ("XIV", "Pearls, Precious Stones, Metals", range(71, 72)),
    ("XV", "Base Metals and Articles of Base Metal", range(72, 84)),
    ("XVI", "Machinery and Electrical Equipment", range(84, 86)),
    ("XVII", "Vehicles, Aircraft, Vessels", range(86, 90)),
    ("XVIII", "Optical, Photographic, Medical Instruments", range(90, 93)),
    ("XIX", "Arms and Ammunition", range(93, 94)),
    ("XX", "Miscellaneous Manufactured Articles", range(94, 97)),
    ("XXI", "Works of Art, Antiques", range(97, 98)),
    ("XXII", "Special Classification Provisions (HTSUS-specific)", range(98, 100)),
]

for roman, name, chapters in _SECTIONS:
    for ch in chapters:
        CHAPTER_TO_SECTION[ch] = (roman, name)


def get_section(chapter: int):
    return CHAPTER_TO_SECTION.get(chapter, (None, None))