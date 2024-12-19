from django.urls import path

from .views import RobotsOrder

urlpatterns = [
    path('', RobotsOrder.as_view(), name='robot-order')
]