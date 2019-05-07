import boto3
import botocore
from app import app
from config import S3_KEY, S3_SECRET, S3_BUCKET
from flask import abort


s3 = boto3.client("s3", aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """Function to upload file to s3"""
    try:
        # ACL stands for access control list
        # ContentType key prevents file from being auto-downloaded when on a public url
        s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={
            "ACL": acl, "ContentType": file.content_type})

    # Catch all exception
    # need appropriate error codes
    except Exception as e:
        return abort(404)

    return f'{app.config["S3_LOCATION"]}{file.filename}'
