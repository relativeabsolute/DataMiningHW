from string import printable

def clean_text(text):
    s = "".join(c for c in text if c in printable)
    return ' '.join(s.split())
