import re

def clean_text(text: str) -> str:

    cleaned_text = re.sub(r'[^A-Za-z0-9-(), ]+', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text