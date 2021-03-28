from collections import OrderedDict
from unittest.mock import Mock, patch

from api.serializers import CarSerializer, RateSerializer
from django.test import TestCase
from rest_framework.serializers import ValidationError


class CarSerializerTestCase(TestCase):
    def setUp(self):
        mock_vpic_validator = Mock()
        mock_UniqueTogetherValidator = Mock()
        self.mock_validators = [mock_vpic_validator, mock_UniqueTogetherValidator]

    def test_serializer_valid_data(self):
        data = {"make": "test_make", "model": "test_model"}

        serializer = CarSerializer(data=data)
        serializer.validators = self.mock_validators
        validity = serializer.is_valid()

        for validator in self.mock_validators:
            validator.assert_called_once_with(serializer.validated_data, serializer)
        self.assertTrue(validity)
        self.assertEqual(
            serializer.validated_data,
            OrderedDict([("make", "test_make"), ("model", "test_model")]),
        )

    def test_serializer_invalid_data(self):
        data = {"make": 51251, "model": None}

        serializer = CarSerializer(data=data)
        serializer.validators = self.mock_validators
        validity = serializer.is_valid()

        for validator in self.mock_validators:
            validator.assert_not_called()

        self.assertFalse(validity)
        self.assertEqual(
            serializer.validated_data,
            {},
        )

    def test_get_avg_rating(self):
        mock_obj = Mock()
        mock_related_set = Mock()
        mock_obj.rate_set = mock_related_set
        mock_related_set.all.return_value = [Mock(rating=i) for i in range(1, 6)]

        result = CarSerializer().get_avg_rating(mock_obj)

        self.assertEqual(result, 3.0)
        mock_related_set.all.assert_called_once_with()

        mock_related_set.reset_mock()
        mock_related_set.all.return_value = []

        result = CarSerializer().get_avg_rating(mock_obj)

        self.assertEqual(result, 0)
        mock_related_set.all.assert_called_once_with()


class RateSerializerTestCase(TestCase):
    def test_serializer_valid_data(self):
        data = {"car_id": 1, "rating": 5}
        serializer = RateSerializer(data=data)
        validity = serializer.is_valid()

        self.assertTrue(validity)
        self.assertEqual(
            serializer.validated_data, OrderedDict([("car_id", 1), ("rating", 5)])
        )

    def test_serializer_invalid_data(self):
        data = {"car_id": 1, "rating": 6}
        serializer = RateSerializer(data=data)
        validity = serializer.is_valid()

        self.assertFalse(validity)
        self.assertEqual(serializer.validated_data, {})

    def test_get_car(self):
        mock_obj = Mock()
        mock_obj.car_id = 123
        serializer = RateSerializer()
        result = serializer.get_car(mock_obj)
        self.assertEqual(result, 123)

    def test_validate_rating(self):
        serializer = RateSerializer()
        result = serializer.validate_rating(1)
        self.assertEqual(result, 1)
        result = serializer.validate_rating(5)
        self.assertEqual(result, 5)

        with self.assertRaisesMessage(ValidationError, "Rating must be in range 1 - 5"):
            serializer.validate_rating(6)

        with self.assertRaisesMessage(ValidationError, "Rating must be in range 1 - 5"):
            serializer.validate_rating(0)
