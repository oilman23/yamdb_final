from datetime import datetime

from django.core.exceptions import ValidationError

YEAR_MIN = 0

SCORE_MIN = 0
SCORE_MAX = 10


def validate_year(value):
    year_max = datetime.now().year
    if not YEAR_MIN <= value <= year_max:
        raise ValidationError(
            'Произведение датировано некорректным годом.'
            f'Корректный диапазон: от {YEAR_MIN} до {year_max}.'
        )


def validate_score(value):
    if not SCORE_MIN <= value <= SCORE_MAX:
        raise ValidationError(
            'Рейтинг произведения некорректен. '
            f'Должен быть в диапазон от {SCORE_MIN} до {SCORE_MAX}'
        )
