from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def validate_username(value):
    regex = r'^[\w.@+-]+\Z'
    if not re.match(regex, value):
        raise ValidationError(
            _('Некорректный формат имени пользователя.'),
            code='invalid_username'
        )
