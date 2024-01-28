from django.contrib import admin
from django.urls import path
from budapi import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tobuda/', views.MarketSpreads.as_view()),
]
