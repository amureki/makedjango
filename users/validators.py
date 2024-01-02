from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    message = _(
        "Enter a valid username. "
        "This value may only contain alphanumeric characters "
        "(letters A-Z, numbers 0-9) with the exception of underscores. "
        "The length of the username must be between 4 and 20 characters."
    )
    regex = "^[A-Za-z0-9_]{4,20}$"


@deconstructible
class EmailValidator(validators.RegexValidator):
    message = _("Enter a valid email address.")
    regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
