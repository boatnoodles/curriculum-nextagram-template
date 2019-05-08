import boto3
import botocore
from app import app
from config import S3_KEY, S3_SECRET, S3_BUCKET, AWS_DOMAIN
from flask import abort, flash, redirect, request, url_for
from time import time
from urllib.parse import urlparse
from werkzeug import secure_filename


s3 = boto3.client("s3", aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_upload(file_form_name, route):
    if file_form_name not in request.files:
        flash("No user_file key in request.files")
        return redirect(url_for(f"{route}.new"))

    file = request.files[file_form_name]

    if file.filename == "":
        flash("Please provide a file name")
        return redirect(url_for(f"{route}.new"))

    if file and allowed_file(file.filename):
        # secure_filename transform " " to "_"
        file.filename = secure_filename(file.filename)
        # Prepend a time stamp to filename to ensure that files with the same name does not get overwritten in S3
        file.filename = str(round(time())) + "_" + file.filename
        return file


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
        print("hehehhehee")
        return redirect(url_for("users.new"))

    return f'{AWS_DOMAIN}/{file.filename}'


def gen_url(file):
    output = upload_file_to_s3(file, S3_BUCKET)
    if output:
        return urlparse(output).path.split('/')[-1]
