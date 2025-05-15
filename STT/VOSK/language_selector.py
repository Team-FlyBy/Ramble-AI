def select_language(ko_text, en_text):
    if len(ko_text) > len(en_text):
        return "ko", ko_text
    elif len(en_text) > 0:
        return "en", en_text
    return None, ""
