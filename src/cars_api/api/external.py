from django.conf import settings

from api.vpic_client import VpicClient

vpic_client = VpicClient(settings.CARS_API_URL)
