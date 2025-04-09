import time
from typing import Dict, Union
from uuid import uuid4
import requests
from io import BytesIO

import boto3
import botocore.exceptions
from botocore import UNSIGNED
from botocore.client import BaseClient
from botocore.config import Config
from django.conf import settings
from django.utils.text import slugify
from pydantic import HttpUrl

from commons.dataclasses import BaseDataClass
from .constant import BucketKey, ContentType

from .utils import is_bucket_public

"""
Singleton S3 Instance
"""
S3_INSTANCE = None
UNSIGNED_S3_INSTANCE = None


class S3Exception(Exception):
    pass


class UploadURLData(BaseDataClass):
    upload_url: HttpUrl
    key: str
    fields: Dict[str, str]


def generate_file_key(file_name: str) -> str:
    return f"{int(time.time())}-{file_name}"


def get_singleton_client(config: Config = None) -> Union[None, BaseClient]:
    global S3_INSTANCE, UNSIGNED_S3_INSTANCE

    if not config:
        if not S3_INSTANCE:
            S3_INSTANCE = boto3.client(
                service_name="s3",
                endpoint_url='https://s3.{}.amazonaws.com'.format(
                    settings.AWS_CONFIG.get("REGION_NAME")),
                region_name=settings.AWS_CONFIG.get("REGION_NAME"),
                aws_access_key_id=settings.AWS_CONFIG.get("ACCESS_KEY_ID"),
                aws_secret_access_key=settings.AWS_CONFIG.get(
                    "SECRET_ACCESS_KEY"),
                config=config,
            )
        return S3_INSTANCE

    if not UNSIGNED_S3_INSTANCE:
        UNSIGNED_S3_INSTANCE = boto3.client(
            service_name="s3",
            endpoint_url='https://s3.{}.amazonaws.com'.format(
                settings.AWS_CONFIG.get("REGION_NAME")),
            region_name=settings.AWS_CONFIG.get("REGION_NAME"),
            aws_access_key_id=settings.AWS_CONFIG.get("ACCESS_KEY_ID"),
            aws_secret_access_key=settings.AWS_CONFIG.get("SECRET_ACCESS_KEY"),
            config=config,
        )

    return UNSIGNED_S3_INSTANCE


def process_url(raw_url: str, bucket_key: BucketKey) -> str:
    # convert url from https://s3.<region-name>.amazonaws.com/bucket-name into https://<bucket-name>.s3.<region-name>.amazonaws.com
    split_url = raw_url.split('/')
    # [https:, '', 'domain', 'path]
    return '{}//{}.{}/'.format(split_url[0], split_url[-1], split_url[2])


def get_upload_link(
    bucket_key: BucketKey, file_name_no_extension: str, file_type: str, expired: int = 900
) -> UploadURLData:
    content_type: ContentType = ContentType[file_type.upper()]
    key = generate_file_key(
        f"{str(uuid4())}-{slugify(file_name_no_extension)}.{file_type}")
    object_key = f"{settings.ENVIRONMENT}/{key}"
    try:
        signed_data = generate_presigned_upload_url(
            bucket_key, object_key, expires_in=expired, content_type=content_type
        )
    except Exception as e:
        settings.LOGGER_INSTANCE.error(f"Upload link key:{key} from S3 - {e}")
        raise S3Exception(str(e)) from e
    return UploadURLData(upload_url=process_url(signed_data["url"], bucket_key), fields=signed_data["fields"], key=object_key)


def generate_presigned_upload_url(
    bucket_key: BucketKey, key: str, expires_in: int, content_type: ContentType = None
):
    """
    Generates a presigned S3 upload URL.
    Returns an S3 bucket URL along with additional params to be sent as part of the upload request:
        `Content-Type, AWSAccessKeyId, policy, signature, key`
    @bucket_key: bucket key in settings
    @key: Object key
    @expires_in: Expiry time of the presigned upload URL
    @content_type: File/extension type.
    """
    client = get_singleton_client()

    fields = {}
    conditions = []

    if content_type:
        fields["Content-Type"] = content_type.value
        conditions.append(["starts-with", "$Content-Type", content_type.value])

    if is_bucket_public(bucket_key):
        fields["acl"] = "public-read"
        conditions.append({"acl": "public-read"})

    return client.generate_presigned_post(
        Bucket=settings.S3_CONFIG.get(bucket_key.value),
        Key=key,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=expires_in,
    )


def get_link(bucket_key: BucketKey, key: str, expired: int = 900) -> str:
    """
    Get URL for an S3 object.
    Public objects (objects with acl: public-read) URL will be static & unsigned.
    Private objects URL on the other hand will be signed and will have expiry time.

    @bucket_key: bucket key in settings
    @key: Object key
    @expires_in: Expiry time of the object URL (private objects only)
    """
    if key == "" or key is None:
        return None
    try:
        link = generate_presigned_object_url(
            bucket_key, key, expires_in=expired)
    except Exception as e:
        settings.LOGGER_INSTANCE.error(f"Get link key:{key} from S3 - {e}")
        raise S3Exception(str(e)) from e
    return link


def generate_presigned_object_url(bucket_key: BucketKey, key: str, expires_in: int) -> str:
    """
    Generates URL for an S3 object.

    @bucket_key: bucket key in settings
    @key: Object key
    @expires_in: Expiry time of the object URL (private objects only)
    """

    if is_bucket_public(bucket_key):
        client = get_singleton_client(
            config=Config(signature_version=UNSIGNED))
    else:
        client = get_singleton_client()

    params = {"Bucket": settings.S3_CONFIG.get(bucket_key.value), "Key": key}

    return client.generate_presigned_url("get_object", Params=params, ExpiresIn=expires_in)


def is_uploaded(bucket_key: BucketKey, path: str) -> bool:
    if is_bucket_public(bucket_key):
        client = get_singleton_client(
            config=Config(signature_version=UNSIGNED))
    else:
        client = get_singleton_client()

    bucket_key = bucket_key.value
    try:
        client.head_object(Bucket=settings.S3_CONFIG.get(bucket_key), Key=path)
        return True
    except botocore.exceptions.ClientError:
        return False


def upload_to_s3_from_url(url: str, bucket_key: BucketKey, path: str) -> str:
    try:
        client = get_singleton_client(
            config=Config(signature_version=UNSIGNED))
        response = requests.get(url)
        img = BytesIO(response.content)
        client.upload_fileobj(
            img, settings.S3_CONFIG.get(bucket_key.value), path)
    except:
        print("============ Error ==============")
        print(url)
        print(path)
        print("=================================")


def upload_to_s3_from_buffer(buffer: BytesIO, bucket_key: BucketKey, path: str, options: dict = None) -> str:
    try:
        client = get_singleton_client(
            config=Config(signature_version=UNSIGNED))
        client.upload_fileobj(
            buffer, settings.S3_CONFIG.get(bucket_key.value), path, ExtraArgs=options)
    except Exception as e:
        print(f"Occurred while uploading sitemap to S3 bucket: {e}")
        print(path)


def upload_to_s3_from_machine(bucket_key: BucketKey, path: str, file_dir: str) -> str:
    client = get_singleton_client(
        config=Config(signature_version=UNSIGNED))

    with open(file_dir, 'rb') as data:
        client.upload_fileobj(
            data, settings.S3_CONFIG.get(bucket_key.value), path)

    return generate_s3_url(bucket_key, path)


def get_file_format_from_url(url: str) -> str:
    return url.split('?')[0].split('.')[-1]


def generate_s3_url(bucket_key: BucketKey, path: str) -> str:
    return f"https://{settings.S3_CONFIG.get(bucket_key.value)}.s3.{settings.AWS_CONFIG.get('REGION_NAME')}.amazonaws.com/{path}"


def get_file_from_bucket(bucket_key: BucketKey, path: str) -> dict:
    """
    Retrieves a file from an S3 bucket.
    Returns the response object containing the file data

    @bucket_key (BucketKey): The BucketKey of target bucket.
    @path (str): The path to the file within the bucket.
    """
    client = get_singleton_client(
        config=Config(signature_version=UNSIGNED))
    try:
        response = client.get_object(
            Bucket=settings.S3_CONFIG.get(bucket_key.value), Key=path)
        return response
    except:
        return None


def get_filenames_in_bucket(bucket_key: BucketKey, path: str = None) -> list:
    """
    Retrieves a list of filenames inside an S3 bucket, 
    or optionally a list of filenames inside a directory within the bucket.
    Returns a list of filenames. 

    @bucket_key (BucketKey): The BucketKey of target bucket.
    @path (str): The path to a directory within the bucket.
    """
    client = get_singleton_client(
        config=Config(signature_version=UNSIGNED))
    filenames = []

    if path is None:
        # List objects at the root of the bucket
        response = client.list_objects_v2(
            Bucket=settings.S3_CONFIG.get(bucket_key.value))
    else:
        # List objects in the specified path
        response = client.list_objects_v2(
            Bucket=settings.S3_CONFIG.get(bucket_key.value), Prefix=path)

    if 'Contents' in response:
        # Extract filenames from the response
        filenames = [obj['Key'] for obj in response['Contents']]

    return filenames
