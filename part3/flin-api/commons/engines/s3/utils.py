from commons.engines.s3.constant import BucketKey

PUBLIC = "public"
PRIVATE = "private"

"""
Refers to S3 Bucket ACL

Public objects (objects with acl: public-read) URL will be static & unsigned.
Private objects URL on the other hand will be signed and will have expiry time.
"""
BUCKET_ACCESS = {
    BucketKey.GENERAL: PUBLIC,
}


def is_bucket_public(bucket_key: BucketKey) -> bool:
    return BUCKET_ACCESS.get(bucket_key) == PUBLIC
