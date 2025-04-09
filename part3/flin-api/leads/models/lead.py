from commons.base_model import BaseModel
from django.db import models

class Lead(BaseModel):

    class LoanType(models.TextChoices):
        PERSONAL = "personal", "Personal Loan"
        KPR = "kpr", "KPR"
        KPA = "kpa", "KPA"

    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    phone_number = models.CharField(max_length=16, blank=True)
    loan_type = models.CharField(max_length=24, choices=LoanType.choices)

    class Meta:
        db_table = "lead"
        verbose_name = "Lead"
        verbose_name_plural = "Leads"