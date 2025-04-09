from enum import Enum


class ContentType(Enum):
    JPG = "image/jpeg"
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"
    GIF = "image/gif"
    PDF = "application/pdf"
    MP4 = "video/mp4"
    AVI = "video/x-msvideo"
    MOV = "video/quicktime"
    MKV = "video/x-matroska"

# TODO


class BucketKey(Enum):
    GENERAL = "BUCKET_GENERAL_PUBLIC"
