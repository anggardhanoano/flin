from django.db import models
from commons.models import Release
from commons.base_model import BaseModel


class ContentModel(BaseModel):
    release = models.OneToOneField(
        Release,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        abstract = True