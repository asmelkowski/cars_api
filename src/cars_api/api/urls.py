from django.urls import path

from api.views import CarsViewSet, PopularView, RateViewSet

urlpatterns = [
    path("cars", CarsViewSet.as_view({"get": "list", "post": "create"})),
    path("cars/<int:pk>", CarsViewSet.as_view({"delete": "destroy"})),
    path("rate", RateViewSet.as_view({"post": "create"})),
    path("popular", PopularView.as_view()),
]
