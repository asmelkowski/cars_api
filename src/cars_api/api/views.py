from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.models import Car, Rate
from api.serializers import CarSerializer, PopularSerializer, RateSerializer


class CarsViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class RateViewSet(ModelViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()


class PopularView(ListAPIView):
    serializer_class = PopularSerializer
    model = Car

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.annotate(rates_number=Count("rate")).order_by("-rates_number")
