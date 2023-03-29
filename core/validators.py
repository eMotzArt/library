from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianPhoneValidator:
    phone_length = 11
    phone_code = 7

    def __call__(self, value):
        if not len(value) == self.phone_length or not int(value[0]) == self.phone_code:
            raise ValidationError('Phone must starts with 7 and have 11 digits')



@deconstructible
class BookNegativeSheetsValidator:

    def __call__(self, value):
        if value < 0:
            raise ValidationError('Sheets count must be positive')

