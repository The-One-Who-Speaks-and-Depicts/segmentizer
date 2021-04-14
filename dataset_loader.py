def load_text(data):
    text = ""
    with open(data, 'r', encoding='utf-8') as inp:
        strings = inp.readlines()
        for s in strings:
            text += s
    text.replace("\n", " ")
    text.replace("\r", " ")
    text.replace("\n-", "")
    text.replace("\r-", "")
    text.replace("  ", " ")
    return text