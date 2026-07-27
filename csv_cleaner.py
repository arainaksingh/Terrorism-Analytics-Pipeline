import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "csv", "GTD.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "gtd_cleaned.csv")


KEEP_COLUMNS = [
    "eventid", "iyear", "imonth", "iday",
    "country_txt", "region_txt", "provstate", "city",
    "latitude", "longitude",
    "attacktype1_txt", "targtype1_txt",
    "gname", "weaptype1_txt",
    "nkill", "nwound",
    "success", "suicide",
    "summary"
]


def load_data():
    print("Loading GTD dataset...")
    df = pd.read_csv(INPUT_PATH, encoding="latin1", low_memory=False)
    print(f"Loaded: {df.shape}")
    return df



def clean_data(df):
    print("Cleaning data...")

    # Keep only useful columns
    df = df[KEEP_COLUMNS]

    # Handle missing numeric values
    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    # Handle missing categorical values
    df["city"] = df["city"].fillna("Unknown")
    df["provstate"] = df["provstate"].fillna("Unknown")
    df["summary"] = df["summary"].fillna("No summary available")

    # Normalize group names
    df["gname"] = df["gname"].replace("Unknown", "Unidentified")

    # Fix invalid dates (0 → 1)
    df["imonth"] = df["imonth"].replace(0, 1)
    df["iday"] = df["iday"].replace(0, 1)

    # Create datetime column
    df["date"] = pd.to_datetime(
        dict(year=df.iyear, month=df.imonth, day=df.iday),
        errors="coerce"
    )

    # Drop invalid dates
    df = df.dropna(subset=["date"])

    # Drop missing coordinates (important for maps)
    df = df.dropna(subset=["latitude", "longitude"])

    # Convert types
    df["nkill"] = df["nkill"].astype(int)
    df["nwound"] = df["nwound"].astype(int)
    df["success"] = df["success"].astype(int)
    df["suicide"] = df["suicide"].astype(int)

    # Remove duplicates
    df = df.drop_duplicates(subset=["eventid"])

    print(f"After cleaning: {df.shape}")

    return df


def add_features(df):
    print("Adding features...")

    # Total casualties
    df["casualties"] = df["nkill"] + df["nwound"]

    # Severity classification
    def classify_severity(x):
        if x == 0:
            return "Low"
        elif x <= 5:
            return "Medium"
        elif x <= 20:
            return "High"
        else:
            return "Critical"

    df["severity"] = df["casualties"].apply(classify_severity)

    return df



def save_data(df):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned data to: {OUTPUT_PATH}")



def main():
    df = load_data()
    df = clean_data(df)
    df = add_features(df)
    save_data(df)
    print("CSV Cleaning Pipeline Completed!")


if __name__ == "__main__":
    main()