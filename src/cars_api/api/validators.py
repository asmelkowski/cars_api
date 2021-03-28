from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ValidationError as DrfValidationError

from api.external import vpic_client


def validate_rating_value(value):
    if value <= 0 or value > 5:
        raise DjangoValidationError(
            "Rating must be in range 1 - 5", params={"rating": value}
        )


def vpic_validator(data):
    vpic_validation_result = vpic_client.validate_model_for_make(
        data["make"], data["model"]
    )
    if not vpic_validation_result:
        raise DrfValidationError("This make and model combination does not exsist.")
