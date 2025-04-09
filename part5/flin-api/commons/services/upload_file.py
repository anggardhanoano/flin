from typing import List, Union

from pydantic import AnyUrl

from commons.engines.s3.constant import BucketKey, ContentType
from commons.constants import BUCKET_NOT_FOUND, NEED_FILE_TYPE, UNKNOWN_FILE_TYPE
from commons.dataclasses import BaseDataClass
from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from commons.engines import s3


class UploadFileRequestData(BaseDataClass):
    file_names: List[str]
    bucket_key: str


class UploadFileURLDataOuter(BaseDataClass):
    class UploadFileURLData(BaseDataClass):
        presigned_data: s3.UploadURLData
        file_name: str
        file_url: Union[str, AnyUrl]
        file_extension: str
        file_path: str

    data: List[UploadFileURLData]

    class Config:
        arbitrary_types_allowed = True


class UploadFileService(Runnable):
    @classmethod
    def run(cls, data: UploadFileRequestData) -> UploadFileURLDataOuter:
        file_names = data.file_names
        upload_urls = []
        try:
            bucket_key_enum = BucketKey[data.bucket_key.upper()]
        except KeyError:
            raise BadRequestException(BUCKET_NOT_FOUND)

        for file_name in file_names:
            file_name_split = file_name.split(".")
            if len(file_name_split) < 2:
                raise BadRequestException(NEED_FILE_TYPE)
            file_type = file_name_split[-1].lower()
            try:
                ContentType[file_type.upper()]
            except KeyError:
                raise BadRequestException(UNKNOWN_FILE_TYPE)

            file_name_no_extension = "".join(file_name_split[:-1])
            upload_url_data = s3.get_upload_link(
                bucket_key_enum, file_name_no_extension, file_type)

            upload_urls.append(
                UploadFileURLDataOuter.UploadFileURLData(
                    presigned_data=upload_url_data,
                    file_name=file_name,
                    file_url=upload_url_data.upload_url,
                    file_extension=file_type,
                    file_path=upload_url_data.key,
                )
            )

        return UploadFileURLDataOuter(data=upload_urls)
