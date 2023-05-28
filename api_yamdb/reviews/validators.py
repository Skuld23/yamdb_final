from datetime import datetime

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if 0 > value > datetime.now().year:
        raise ValidationError(f'{value} некорректный год!')


def score_validator(value):
    if 0 > value or value > 10:
        raise ValidationError(f'{value} некорректная оценка!')
