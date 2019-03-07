import datetime

from django.core.validators import MinValueValidator, deconstructible
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


@deconstructible
class DateValidator(MinValueValidator):
    message = _('Ensure this date is greater than or equal to %(limit_value)s.')
    code = 'min_date'

    def __init__(self, limit_value=None, message=None):
        limit_value = limit_value or self.default()
        super().__init__(limit_value, message)

    def compare(self, a, b):
        return super().compare(self.get_date(a), self.get_date(b))

    @staticmethod
    def default():
        return timezone.now().date()

    @staticmethod
    def get_date(value):
        if callable(value):
            value = value()
        if isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, datetime.date):
            return value
        else:
            raise TypeError("limit_value must date or datetime class "
                            "or callable that return ont of this types.")
