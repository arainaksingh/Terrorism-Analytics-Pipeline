import os
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEXT_DIR = os.path.join(BASE_DIR, "data", "raw", "text")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "text_entities.csv")

# Threat-related keywords (custom intelligence logic)
THREAT_KEYWORDS = [
    "bomb", "blast", "attack", "explosion",
    "gunfire", "terrorist", "hostage", "militant"
]



def extract_entities(text, source_file):
    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "source": source_file,
            "entity": ent.text,
            "label": ent.label_
        })

    # Keyword extraction
    text_lower = text.lower()
    for keyword in THREAT_KEYWORDS:
        if keyword in text_lower:
            entities.append({
                "source": source_file,
                "entity": keyword,
                "label": "THREAT_KEYWORD"
            })

    return entities



def process_files():
    print("Processing text files...")

    all_entities = []

    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            file_path = os.path.join(TEXT_DIR, file)

            print(f"Processing: {file}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            entities = extract_entities(text, file)
            all_entities.extend(entities)

    return pd.DataFrame(all_entities)



def save_data(df):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to: {OUTPUT_FILE}")



def main():
    df = process_files()

    if df.empty:
        print("No entities extracted.")
    else:
        save_data(df)
        print("Text entity extraction completed!")


if __name__ == "__main__":
    main()