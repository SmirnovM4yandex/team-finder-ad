from django.core.validators import RegexValidator

from .constants import (
    GITHUB_ERROR_MESSAGE,
    GITHUB_REGEX,
    PHONE_ERROR_MESSAGE,
    PHONE_REGEX,
)


phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message=PHONE_ERROR_MESSAGE,
)

github_validator = RegexValidator(
    regex=GITHUB_REGEX,
    message=GITHUB_ERROR_MESSAGE,
)
