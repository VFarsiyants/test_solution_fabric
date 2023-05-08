import re
import pytz

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone(value):
    pattern = r'^7\d{10}$'
    if not re.match(pattern, value):
        raise ValidationError("Неккоректный формат номера телефона")
    

def validate_timezone(value):
    if not value in pytz.all_timezones:
        raise ValidationError('Неккоректный формат часового пояса')


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11, 
        verbose_name='Номер телефона клиента',
        validators=[validate_phone]
    )
    mobile_code = models.PositiveSmallIntegerField(
        verbose_name='Код мобильного оператора',
        validators=[MinValueValidator(900), MaxValueValidator(999)]
    )

    tag = models.CharField(
        max_length=50,
        verbose_name='Тэг (произвольная метка)'
    )

    timezone = models.CharField(
        max_length=255,
        validators=[validate_timezone]
    )
