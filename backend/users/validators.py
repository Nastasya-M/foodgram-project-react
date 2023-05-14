import re

from django.core.exceptions import ValidationError


def username_validator(value):
    symbol = ''.join(set(re.sub(r'[\w.@+-]', '', value)))
    if value == 'me':
        raise ValidationError(
            'Имя "me" в качестве username запрещено')
    if symbol:
        raise ValidationError(
            f'Запрещено использование {symbol} в имени')
    return value
