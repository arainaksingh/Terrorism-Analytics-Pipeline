import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GTD_FILE = os.path.join(BASE_DIR, "data", "processed", "gtd_cleaned.csv")
TEXT_FILE = os.path.join(BASE_DIR, "data", "processed", "text_entities.csv")
VIDEO_FILE = os.path.join(BASE_DIR, "data", "processed", "video_metadata.csv")

OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "unified_data.csv")


def load_data():
    print("Loading datasets...")
    gtd = pd.read_csv(GTD_FILE)
    text = pd.read_csv(TEXT_FILE)
    video = pd.read_csv(VIDEO_FILE)
    return gtd, text, video


def clean_text(value):
    """Remove newlines and commas for safe CSV writing"""
    if pd.isna(value):
        return ""
    return str(value).replace("\n", " ").replace(",", " ").strip()


def keyword_match(text_entities, summary):
    if pd.isna(summary):
        return False

    summary = summary.lower()

    for entity in text_entities:
        if isinstance(entity, str) and entity.lower() in summary:
            return True

    return False


def map_text_to_gtd(gtd, text):
    print("Mapping TEXT → GTD...")

    grouped = text.groupby("source")["entity"].apply(list).reset_index()
    mappings = []

    for _, row in grouped.iterrows():
        entities = row["entity"]

        for _, gtd_row in gtd.iterrows():

            location_match = any(
                str(ent).lower() in str(gtd_row["city"]).lower()
                or str(ent).lower() in str(gtd_row["country_txt"]).lower()
                for ent in entities
            )

            keyword_flag = keyword_match(entities, gtd_row["summary"])

            if location_match or keyword_flag:
                clean_entities = [clean_text(e) for e in entities]

                mappings.append({
                    "eventid": gtd_row["eventid"],
                    "city": clean_text(gtd_row["city"]),
                    "country": clean_text(gtd_row["country_txt"]),
                    "date": gtd_row["date"],
                    "attack_type": clean_text(gtd_row["attacktype1_txt"]),
                    "group": clean_text(gtd_row["gname"]),
                    "casualties": gtd_row["casualties"],
                    "severity": clean_text(gtd_row["severity"]),
                    "source_file": clean_text(row["source"]),
                    "matched_entities": " | ".join(clean_entities)
                })

    return pd.DataFrame(mappings)


def map_video(video_df, mapped_df):
    print("Mapping VIDEO → EVENTS...")

    if video_df.empty or mapped_df.empty:
        return mapped_df

    video_df = video_df.copy()
    mapped_df = mapped_df.copy()

    video_df["key"] = 1
    mapped_df["key"] = 1

    merged = pd.merge(mapped_df, video_df, on="key").drop("key", axis=1)

    return merged


def save_data(df):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Final cleaning before save
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace("\n", " ")

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved unified data to: {OUTPUT_FILE}")


def main():
    gtd, text, video = load_data()

    mapped_text = map_text_to_gtd(gtd, text)
    unified = map_video(video, mapped_text)

    if unified.empty:
        print("No mappings found.")
    else:
        save_data(unified)
        print("Schema mapping completed!")


if __name__ == "__main__":
    main()