from django.contrib import admin
from django.urls import path

from budapi import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/tobuda/", views.SingleMarketSpread.as_view()),
    path("api/tobuda/all/", views.EveryMarketSpread.as_view()),
]
