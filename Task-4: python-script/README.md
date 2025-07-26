# S3 Large File Uploader

Upload large or small files to Amazon S3 with optional multipart upload, logging, and presigned URL generation.

# Setup
requirements : boto3, PyYAML
pip install -r requirements.txt

# Basic Upload

python upload/to/s3.py --file path/to/file.txt --bucket bucket-name

# With AWS CLI

python upload/to/s3.py --file path/to/file.txt --bucket bucket-name --profile default

# Use YAML Config

python upload/to/s3.py --config upload/config.yaml

# Generate Presigned URL

python upload/to/s3.py --file path/to/file.txt --bucket bucket-name --presign
