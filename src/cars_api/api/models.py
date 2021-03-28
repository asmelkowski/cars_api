from django.core.exceptions import ValidationError
from django.db import models

from api.validators import validate_rating_value


class Car(models.Model):
    make = models.CharField(max_length=64, null=False, blank=False)
    model = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return f"{self.pk}. {self.make}, {self.model}"

    class Meta:
        unique_together = ["make", "model"]


class Rate(models.Model):

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[validate_rating_value])
