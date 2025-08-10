import spacy

NLP = spacy.load("ru_core_news_sm")

def simplify_line(line: str) -> str:
    """Simplify line with spacy"""
    doc = NLP(line)
    # keep lemmas, do not skip punctuation and prepositions
    string = ''
    for token in doc:
        if token.is_punct:
            string = string + token.text + ' '
        else:
            string = string + token.pos_ + ' '
    return string