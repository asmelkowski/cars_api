from api import urls as api_url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("api/", include(api_url))]
