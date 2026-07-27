import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "unified_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "partitioned")


def partition_by_year():
    print("📥 Loading unified data...")
    df = pd.read_csv(INPUT_FILE)

    print("🧹 Cleaning data...")
    # Remove newlines and trim spaces
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace("\n", " ").str.strip()

    print("📅 Converting date column...")
    df["date"] = pd.to_datetime(df["date"], errors='coerce')

    print("➕ Adding year column...")
    df["year"] = df["date"].dt.year

    # Drop invalid rows
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    print("📂 Partitioning by year...")

    total_partitions = 0

    for year, group in df.groupby("year"):
        partition_path = os.path.join(OUTPUT_DIR, f"year={year}")
        os.makedirs(partition_path, exist_ok=True)

        file_path = os.path.join(partition_path, "data.csv")

        # IMPORTANT: Save without index, proper encoding
        group.to_csv(file_path, index=False, encoding="utf-8")

        print(f"✅ Saved partition: {file_path}")
        total_partitions += 1

    print(f"\n🎯 Total partitions created: {total_partitions}")
    print("🚀 Data is ready for S3 upload and Athena querying!")


if __name__ == "__main__":
    partition_by_year()