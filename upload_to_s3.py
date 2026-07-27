import os
import boto3

BUCKET_NAME = "terrorism-analytics-ashmit-04042026"  
S3_PREFIX = "processed/unified_data/" 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_PARTITION_DIR = os.path.join(BASE_DIR, "data", "partitioned")


def upload_folder_to_s3():
    print("🚀 Starting upload to S3...")

    s3_client = boto3.client("s3")

    total_files = 0

    for root, dirs, files in os.walk(LOCAL_PARTITION_DIR):
        for file in files:
            local_path = os.path.join(root, file)

            # Get relative path (important for partition structure)
            relative_path = os.path.relpath(local_path, LOCAL_PARTITION_DIR)

            # Convert to S3 key
            s3_key = os.path.join(S3_PREFIX, relative_path).replace("\\", "/")

            try:
                s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
                print(f"✅ Uploaded: s3://{BUCKET_NAME}/{s3_key}")
                total_files += 1
            except Exception as e:
                print(f"❌ Failed: {local_path}")
                print(e)

    print(f"\n🎯 Upload complete! Total files uploaded: {total_files}")


if __name__ == "__main__":
    upload_folder_to_s3()