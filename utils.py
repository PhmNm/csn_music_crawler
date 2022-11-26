from unidecode import unidecode
import re

VIETNAMESE_PATTERN = {
    "[àáảãạăắằẵặẳâầấậẫẩ]": "a",
    "[ÀÁẢÃẠĂẮẰẴẶẲÂẦẤẬẪẨ]": "A",
    "[đ]": "d",
    "[Đ]": "D",
    "[èéẻẽẹêềếểễệ]": "e",
    "[ÈÉẺẼẸÊỀẾỂỄỆ]": "E",
    "[ìíỉĩị]": "i",
    "[ÌÍỈĨỊ]": "I",
    "[òóỏõọôồốổỗộơờớởỡợ]": "o",
    "[ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ]": "O",
    "[ùúủũụưừứửữự]": "u",
    "[ÙÚỦŨỤƯỪỨỬỮỰ]": "U",
    "[ỳýỷỹỵ]": "y",
    "[ỲÝỶỸỴ]": "Y",
}

def convert_accented_vietnamese_text(data, lower=True):
    if not data:
        return ""
    if lower is True:
        data = data.lower()
    data = unidecode(data)
    for regex, replace in VIETNAMESE_PATTERN.items():
        data = re.sub(regex, replace, data)

    data = data.replace("\n", " ")
    return data