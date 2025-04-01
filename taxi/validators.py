from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class ExactLenValidator(BaseValidator):
    message = _(
        "Ensure this value has exactly %(limit_value)s "
        "characters (it has %(show_value)s)."
    )
    code = "exact_length"

    def clean(self, value):
        return len(value)

    def compare(self, input_length, required_length):
        return input_length != required_length


class FirstUpperLetter(BaseValidator):
    message = _(
        "Ensure the first characters %(limit_value)s are uppercase letters."
    )
    code = "first_upper"

    def compare(self, value, required_count):
        first_part = value[:required_count]
        return not (first_part.isupper() and first_part.isalpha())


class LastDigits(BaseValidator):
    message = _("Ensure the last %(limit_value)s characters are digits.")
    code = "last_digits"

    def compare(self, value, required_count):
        last_part_digit = value[-required_count:]
        return not last_part_digit.isdigit()
