from django.db.models import DecimalField


class BaseDecimalField(DecimalField):
    def __init__(self, decimal_places=2, max_digits=14, default=0, **kwargs):
        super().__init__(decimal_places=decimal_places, max_digits=max_digits, default=default, **kwargs)
