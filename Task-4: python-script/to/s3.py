import os
import sys
import boto3
import logging
import argparse
import yaml
from botocore.exceptions import ClientError
from datetime import datetime

# Constants
MULTIPART_THRESHOLD = 100 * 1024 * 1024  # 100MB
LOG_FILE = "upload.log"

# Logging setup
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_status(file_path, size, status):
    timestamp = datetime.now().isoformat()
    logging.info(f"{file_path} | {size} bytes | {status} | {timestamp}")


def get_s3_client(profile=None):
    if profile:
        session = boto3.Session(profile_name=profile)
        return session.client('s3')
    return boto3.client('s3')


def multipart_upload(s3_client, file_path, bucket, key):
    try:
        transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_threshold=MULTIPART_THRESHOLD
        )
        s3_resource = boto3.resource('s3')
        s3_resource.meta.client.upload_file(
            Filename=file_path,
            Bucket=bucket,
            Key=key,
            Config=transfer_config
        )
        log_status(file_path, os.path.getsize(file_path), "Multipart Upload Successful")
    except Exception as e:
        log_status(file_path, os.path.getsize(file_path), f"Multipart Upload Failed: {e}")
        raise


def simple_upload(s3_client, file_path, bucket, key):
    try:
        with open(file_path, 'rb') as f:
            s3_client.upload_fileobj(f, bucket, key)
        log_status(file_path, os.path.getsize(file_path), "Upload Successful")
    except Exception as e:
        log_status(file_path, os.path.getsize(file_path), f"Upload Failed: {e}")
        raise


def upload_file(s3_client, file_path, bucket, key):
    file_size = os.path.getsize(file_path)
    if file_size > MULTIPART_THRESHOLD:
        multipart_upload(s3_client, file_path, bucket, key)
    else:
        simple_upload(s3_client, file_path, bucket, key)


def generate_presigned_url(s3_client, bucket, key, expiry=3600):
    return s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket, 'Key': key},
                                            ExpiresIn=expiry)


def upload_directory(s3_client, folder_path, bucket, prefix=""):
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            s3_key = os.path.join(prefix, relative_path).replace("\\", "/")
            upload_file(s3_client, full_path, bucket, s3_key)


def main():
    parser = argparse.ArgumentParser(description="Upload files to S3 with optional multipart support.")
    parser.add_argument('--file', help='Path to file or folder')
    parser.add_argument('--bucket', help='S3 bucket name')
    parser.add_argument('--key', help='Destination key in S3')
    parser.add_argument('--profile', help='AWS CLI profile to use')
    parser.add_argument('--config', help='Path to YAML config file')
    parser.add_argument('--presign', action='store_true', help='Generate presigned URL')

    args = parser.parse_args()

    # Read config if provided
    if args.config:
        with open(args.config) as f:
            config = yaml.safe_load(f)
            args = argparse.Namespace(**{**vars(args), **config})

    if not args.file or not args.bucket:
        print("Error: --file and --bucket are required arguments.")
        sys.exit(1)

    s3_client = get_s3_client(args.profile)

    if os.path.isdir(args.file):
        upload_directory(s3_client, args.file, args.bucket, args.key or "")
    else:
        final_key = args.key or os.path.basename(args.file)
        upload_file(s3_client, args.file, args.bucket, final_key)

        if args.presign:
            url = generate_presigned_url(s3_client, args.bucket, final_key)
            print(f"Presigned URL: {url}")


if __name__ == '__main__':
    main()
