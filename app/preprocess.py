import re


def clean_text(text: str) -> str:
    text = text.replace("\t", " ")
    text = re.sub(r"[ ]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()
def preprocess_document(document: dict) -> dict:
    cleaned_document = document.copy()

    cleaned_document["text"] = clean_text(document["text"])

    return cleaned_document
if __name__ == "__main__":
    sample_text = """
    CirQX       is an AI-powered platform.


    It helps retailers\tmanage inventory.



    It also supports recycling.
    """

    cleaned_text = clean_text(sample_text)

    print("RAW TEXT:")
    print(sample_text)

    print("\nCLEANED TEXT:")
    print(cleaned_text)