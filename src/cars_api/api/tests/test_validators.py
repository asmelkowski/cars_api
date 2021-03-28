from unittest.mock import patch

from api.validators import validate_rating_value, vpic_validator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.test import TestCase
from rest_framework.serializers import ValidationError as DrfValidationError

PATCHING_PATH = "api.validators"


class ValidatorsTestCase(TestCase):
    def test_validate_rating_value(self):
        with self.assertRaises(DjangoValidationError) as ctx:
            validate_rating_value(0)
        self.assertEqual(ctx.exception.message, "Rating must be in range 1 - 5")
        self.assertEqual(ctx.exception.params, {"rating": 0})

        with self.assertRaises(DjangoValidationError) as ctx:
            validate_rating_value(6)
        self.assertEqual(ctx.exception.message, "Rating must be in range 1 - 5")
        self.assertEqual(ctx.exception.params, {"rating": 6})

        self.assertIsNone(validate_rating_value(1))
        self.assertIsNone(validate_rating_value(5))

    @patch(f"{PATCHING_PATH}.vpic_client")
    def test_vpic_validator(self, mock_vpic_client):
        mock_vpic_client.validate_model_for_make.return_value = True
        self.assertIsNone(vpic_validator({"make": "ford", "model": "focus"}))
        mock_vpic_client.validate_model_for_make.assert_called_once_with(
            "ford", "focus"
        )
        mock_vpic_client.reset_mock()
        mock_vpic_client.validate_model_for_make.return_value = False
        with self.assertRaises(DrfValidationError) as ctx:
            vpic_validator({"make": "ford", "model": "shmockcus"})
        mock_vpic_client.validate_model_for_make.assert_called_once_with(
            "ford", "shmockcus"
        )
        self.assertEqual(
            str(ctx.exception),
            "[ErrorDetail(string='This make and model combination does not exsist.', code='invalid')]",
        )
