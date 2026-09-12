# very preemptive mapping of HTS chapter ranges to affected industries/sectors.
# not exhaustive or confirmed, need to come back to this

CHAPTER_SECTOR_MAP = {
    range(1, 6): "Agriculture / Livestock",
    range(6, 15): "Agriculture / Produce",
    range(15, 16): "Food Processing / Edible Oils",
    range(16, 25): "Food & Beverage",
    range(25, 28): "Mining / Minerals",
    range(28, 39): "Chemicals",
    range(39, 41): "Plastics & Rubber",
    range(41, 44): "Leather & Furskins",
    range(44, 47): "Wood & Forestry Products",
    range(47, 50): "Paper & Pulp",
    range(50, 64): "Textiles & Apparel",
    range(64, 68): "Footwear & Accessories",
    range(68, 71): "Glass, Ceramics, Stone",
    range(71, 72): "Jewelry & Precious Metals",
    range(72, 84): "Metals & Metal Products",
    range(84, 86): "Machinery & Electronics",
    range(86, 90): "Automotive, Aerospace, Transport",
    range(90, 93): "Medical & Optical Instruments",
    range(93, 94): "Defense / Arms",
    range(94, 97): "Furniture & Miscellaneous Manufacturing",
    range(97, 98): "Art & Antiques",
    range(98, 100): "Special/Administrative Provisions",
}


def get_sector(chapter: str) -> str:
    if not chapter or not chapter.isdigit():
        return "Unknown sector"
    chapter_num = int(chapter)
    for chapter_range, sector in CHAPTER_SECTOR_MAP.items():
        if chapter_num in chapter_range:
            return sector
    return "Unknown sector"