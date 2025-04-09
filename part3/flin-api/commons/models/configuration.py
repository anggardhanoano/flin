from django.db import models

from commons.base_model import BaseModel


class Configuration(BaseModel):
    key = models.CharField(unique=True, max_length=256)
    content = models.JSONField()

    class Meta:
        db_table = "configuration"
        verbose_name = "Configuration"

    def __str__(self) -> str:
        return self.key
