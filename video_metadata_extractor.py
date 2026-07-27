import cv2
import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VIDEO_DIR = os.path.join(BASE_DIR, "data", "raw", "video")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "video_metadata.csv")


def extract_video_metadata(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Failed to open {video_path}")
        return None

    # Metadata extraction
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    return {
        "file_name": os.path.basename(video_path),
        "fps": round(fps, 2),
        "frame_count": frame_count,
        "duration_sec": round(duration, 2),
        "resolution": f"{width}x{height}"
    }

def process_videos():
    print("Processing videos...")

    results = []

    for file in os.listdir(VIDEO_DIR):
        if file.endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_path = os.path.join(VIDEO_DIR, file)

            print(f"Processing: {file}")
            metadata = extract_video_metadata(video_path)

            if metadata:
                results.append(metadata)

    return pd.DataFrame(results)



def save_data(df):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved metadata to: {OUTPUT_FILE}")



def main():
    df = process_videos()

    if df.empty:
        print("No video metadata extracted.")
    else:
        save_data(df)
        print("Video metadata extraction completed!")


if __name__ == "__main__":
    main()