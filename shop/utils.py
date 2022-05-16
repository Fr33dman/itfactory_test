from rest_framework import serializers


def normalize_phone_number(phone_number: str) -> str:
    if phone_number.startswith('+') and len(phone_number) == 12:
        phone_number = f'8{phone_number[2:]}'
    return phone_number


def validate_phone_number(phone):
    phone_validation_error = serializers.ValidationError(
            'Номер телефона должен быть длинной 11 или 12 символов и соответствовать форматам: '
            '+79990000000 или 89990000000'
        )
    if len(phone) < 11 or len(phone) > 12:
        raise phone_validation_error
    phone = normalize_phone_number(phone)
    if not phone.isdigit():
        raise phone_validation_error
    return phone
